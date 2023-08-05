import collections
import os
import shutil
import subprocess
import yaml

from typing import Any, Dict, List, Optional

from .PackerTemplate import PackerTemplate

class TemplatesSelectionError(Exception):
    pass

class Packman:
    """This class implements the Packman engine for generating packer template json files and run packer optionally .
    """

    def __init__(self, input_file: str, templates_base_dir: Optional[str] = None, packages_base_dir: Optional[str] = None) -> None:
        """Constructor.

        Parameters
        ----------
        input_file: str
            Path to the Packman input file.
        """

        # The base directory for templates
        self._templates_base_dir = os.path.abspath(templates_base_dir) if templates_base_dir is not None else os.path.join(os.getcwd(),"templates")

        # The base directory for packages
        self._packages_base_dir = os.path.abspath(packages_base_dir) if packages_base_dir is not None else os.path.join(os.getcwd(),"packages")

        with open(input_file, "r") as fin:
            data = yaml.safe_load(fin)

        # The input file must ne a YAML file which declares a 'templates' dictionary
        if "templates" not in data:
            raise IOError("Invalid YAML file: must contains 'templates' tag")

        self._templates = data["templates"]

    def get_templates_selection(self, selected_templates = None):
        """Filter out a template selection from those which are not actual ones.

        Parameters
        ----------
        template_name: str
            The name of the template to fetch.

        Returns
        -------
        list
            The filtered templates list.
        """

        if selected_templates is None:
            selected_templates = ["*"]

        # If '*' is in the list of the selected templates, pick all the templates found in the templates base directory
        if "*" in selected_templates:
            templates = self._templates.keys()
        else:
            # Filter out the image names not present in the yaml file
            templates = [template for template in selected_templates if template in self._templates]
            if not selected_templates:
                raise TemplatesSelectionError("Empty templates selection")


        return templates

    def get_template(self, template_name):
        """Return the YAML contents of a given template.
        :class:`.PackerTemplate`

        Parameters
        ----------
        selected_templates: list, optional
            List of strings corresponding to the packer templates from which the hierarchy should be built.

        Returns
        -------
        list
            Returns the hierarchy of templates from the one with no parent to the ones with parents.
        """

        return self._templates[template_name] if isinstance(self._templates[template_name],dict) else {}

    def _build_template(self, template_name : str) -> PackerTemplate:
        """Build a PackerTemplate object from a template name.

        Parameters
        ----------
        template_name: str
            The name of the template to build.

        Returns
        -------
        :class:`.PackerTemplate`

            The template object used by packman to build the manifest.json file.        
        """

        # Fetch the template matching template_name key
        template_node = self.get_template(template_name)

        # Build the path for the template manifest file (YAML)
        manifest_file = os.path.join(self._templates_base_dir,template_name,"manifest.yml")
        
        # Opens the file and load its contents
        try:
          fin = open(manifest_file, "r")
        # If the file does not exist, the manifest contents is just an empty dict
        except FileNotFoundError:
            manifest_data : Dict[str,str] = {}
        else:
            manifest_data = yaml.safe_load(fin)

        # Get the packages node which gives the list of non-standard applications to add to the packer process 
        packages = template_node.get("packages", [])

        # Build a PackerTemplate object that can be dumped to a manifest.json file
        template = PackerTemplate(template_name, manifest_data, packages, self._packages_base_dir, self._templates_base_dir)

        return template

    def _build_template_hierarchy(self, template_name : str, hierarchy : List[str]):
        """Build a single template hierarchy.

        A template can have a parent template. In that case for packer neig able to run on those templates, 
        the parent tenplate must have been built before.

        Getting a hierarchy of templates, the first one being  the ones with no parent is the goal of this method.

        Parameters
        ----------
        template_name: str
            The template on which the hierarchy will be built upon.

        hierarchy: list
            A list of strings corresponding tot the template hierarchy.

            This argument is just used for passing the template hierarchy across recursive calls of this method. 
        """

        # Fetch the template matching template_name key
        template_node = self.get_template(template_name)

        extends = template_node.get("extends",None)

        hierarchy.append(template_name)

        if extends is None:
            return

        else:
            self._build_template_hierarchy(extends, hierarchy)
            
    def _build_config_hierarchy(self, selected_templates : Optional[List[str]] = None):
        """Build the templates hierarchy.

        A template can have a parent template. In that case for packer neig able to run on those templates, 
        the parent tenplate must have been built before.

        Getting a hierarchy of templates, the first one being  the ones with no parent is the goal of this method.

        Parameters
        ----------
        selected_templates: list, optional
            List of strings corresponding to the packer templates from which the hierarchy should be built.

        Returns
        -------
        list
            Returns the hierarchy of templates from the one with no parent to the ones with parents.
        """

        templates = self.get_templates_selection(selected_templates)

        config_hierarchy : List[str] = []
        for template in templates:
            self._build_template_hierarchy(template, config_hierarchy)

        config_hierarchy.reverse()
        config_hierarchy = list(collections.OrderedDict.fromkeys(config_hierarchy))

        return config_hierarchy

    def run(self, selected_templates : Optional[List[str]] = None, log : Optional[bool] = False, key_rate: Optional[int] = 10):
        """Run packer on the generated manifest.json files.

        Parameters
        ----------
        selected_templates: list, optional
            The packer templates to run with packer.
        """

        # Check first that packer program is installed somewhere
        if shutil.which("packer") is None:
            raise FileNotFoundError("packer could not be found.")

        if key_rate < 10:
            raise ValueError("The key rate is too low. This will trigger input error.")

        # Set env variables for packer run environment
        packer_env = os.environ.copy()
        # This allow to speed up the typing of the preseed command line
        packer_env["PACKER_KEY_INTERVAL"] = "{}ms".format(key_rate)
        # This will add log output for packer run    
        packer_env["PACKER_LOG"] = "1" if log else "0"

        # Define the template hierarchy for the selected templates
        config_hierarchy = self._build_config_hierarchy(selected_templates)

        # Save the current directory
        current_dir = os.getcwd()

        # Loop over the template hierarchy and run packer
        for template in config_hierarchy:

            # cd to the the template directory
            current_template_dir = os.path.join(self._templates_base_dir,template)

            build_dir = os.path.join(current_template_dir,"builds")

            if os.path.exists(build_dir):
                print(f"packer build already found in {current_template_dir}. Skip packer run for that template.")
                continue
            else:
                print(f"Building image for {template}:")

            os.chdir(current_template_dir)

            # Run packer upon the manifest.json file
            manifest_json = os.path.join(current_template_dir,"manifest.json")
            subprocess.call(["packer","build",manifest_json], env=packer_env)

        # cd back to the current dir
        os.chdir(current_dir)
                    
    def build(self, selected_templates : Optional[List[str]] = None, **kwargs):
        """Build packer on the generated manifest.json files.

        Parameters
        ----------
        selected_templates: list, optional
            List of strings corresponding to the packer templates to build.

        run: bool, optional
            If True packer will be run from the generated manifest.json files.
        """

        templates = self.get_templates_selection(selected_templates)

        if not templates:
            raise RuntimeError("Invalid or empty template selection")

        # Loop over the selected templates
        for template_name in templates:

            template = self._build_template(template_name)
            template_node = self.get_template(template_name)

            # Fetch the parent template if any
            parent_template = template_node.get("extends", None)
            if parent_template is not None:
                parent_template = self._build_template(parent_template)
                template.set_parent(parent_template)

            # Dump the template
            output_file = os.path.join(self._templates_base_dir,template_name,"manifest.json")
            template.dump(output_file,**kwargs)

