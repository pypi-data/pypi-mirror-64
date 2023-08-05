#%% modules
import cv2, copy, os, sys, warnings
import numpy as np
import pandas as pd

import pickle
import platform
import pprint
import subprocess
import time
import ruamel.yaml

from datetime import datetime
from ruamel.yaml.comments import CommentedMap as ordereddict
from shutil import copyfile, rmtree

from phenopype import presets
from phenopype.settings import *
from phenopype.core import preprocessing, segmentation, measurement, export, visualization
from phenopype.utils import load_image, load_directory, load_image_data, load_meta_data
from phenopype.utils_lowlevel import _image_viewer, _del_rw, _file_walker, _load_pype_config, _create_generic_pype_config
from phenopype.utils_lowlevel import _load_yaml, _show_yaml, _save_yaml, _yaml_file_monitor

#%% settings

pd.options.display.max_rows = 10 # how many rows of pd-dataframe to show
pretty = pprint.PrettyPrinter(width=30) # pretty print short strings
ruamel.yaml.Representer.add_representer(ordereddict, ruamel.yaml.Representer.represent_dict) # suppress !!omap node info


#%% classes

class project: 
    """
    Initialize a phenopype project with a root directory path. Phenopype 
    will create the project folder at the provided location. 

    Parameters
    ----------

    rootdir: str
        path to root directory of the project where folder gets created
    overwrite: bool, optional
        overwrite option, if a given root directory already exist 
        (WARNING: also removes all folders inside)

    Returns
    -------

    None
    """
    def __init__(self, root_dir, overwrite=False):

        ## kwargs
        flag_overwrite = overwrite

        ## feedback
        print("--------------------------------------------")
        print("phenopype will create a new project at:\n")
        print(root_dir)

        ## decision tree if directory exists
        while True:
            create = input("Proceed? (y/n)\n")
            if create=="y" or create == "yes":
                if os.path.isdir(root_dir):
                    if flag_overwrite == True:
                        rmtree(root_dir, onerror=_del_rw) 
                        print("\n\"" + root_dir + "\" created (overwritten)")
                        pass
                    else:
                        overwrite = input("Warning - project root_dir already exists - overwrite? (y/n)")
                        if overwrite == "y" or overwrite == "yes":
                            rmtree(root_dir, onerror=_del_rw) 
                            print("\n\"" + root_dir + "\" created (overwritten)")
                            pass
                        else:
                            print("\n\"" + root_dir + "\" not created!")
                            print("--------------------------------------------")    
                            break
                else:
                    pass
            else:
                print("\n\"" + root_dir + "\" not created!")
                break

            ## make directories
            self.root_dir = root_dir
            os.makedirs(self.root_dir)
            self.data_dir = os.path.join(self.root_dir, "data")
            os.makedirs(self.data_dir)

            ## lists for files to add
            self.dirnames = []
            self.dirpaths = []
            self.filenames = []
            self.filepaths = []

            ## global project attributes
            project_data = {
                "date_created": datetime.today().strftime('%Y%m%d_%H%M%S'),
                "date_changed": datetime.today().strftime('%Y%m%d_%H%M%S'),
                "root_dir": self.root_dir,
                "data_dir": self.data_dir}

            _save_yaml(project_data, os.path.join(self.root_dir, "attributes.yaml"))

            print("\nproject attributes written to " + os.path.join(self.root_dir, "attributes.yaml"))
            print("--------------------------------------------")
            break

    def add_files(self, image_dir, filetypes=default_filetypes, include=[], exclude=[],
                  raw_mode="copy", search_mode="dir", unique_mode="path", overwrite=False,
                  resize=1, **kwargs):
        """
        Add files to your project from a directory, can look recursively. 
        Specify in- or exclude arguments, filetypes, duplicate-action and copy 
        or link raw files to save memory on the harddrive. For each found image,
        a folder will be created in the "data" folder within the projects root
        directory. If found images are in subfolders and search_mode is 
        recursive, the respective phenopype directories will be created with 
        flattened path as prefix. E.g., with "raw_files" as folder with the original
        image files and "phenopype_proj" as rootfolder:
        
        raw_files/file.jpg ==> phenopype_proj/data/file.jpg
        raw_files/subdir1/file.jpg ==> phenopype_proj/data/1__subdir1__file.jpg
        raw_files/subdir1/subdir2/file.jpg ==> phenopype_proj/data/2__subdir1__subdir2__file.jpg
    
        Parameters
        ----------
    
        image_dir: str 
            path to directory with images
        filetypes: list or str, optional
            single or multiple string patterns to target files with certain endings
        include: list or str, optional
            single or multiple string patterns to target certain files to include
        exclude: list or str, optional
            single or multiple string patterns to target certain files to exclude - 
            can overrule "include"
        raw_mode: {"copy", "link"} str, optional
            how should the raw files be passed on to the phenopype directory tree: 
            "copy" will make a copy of the original file, "link" will only send the 
            link to the original raw file to attributes, but not copy the actual 
            file (useful for big files)
        search_mode: {"dir", "recursive"}, str, optional
            "dir" searches current directory for valid files; "recursive" walks 
            through all subdirectories
        unique_mode: {"filepath", "filename"}, str, optional:
            how to deal with image duplicates - "filepath" is useful if identically 
            named files exist in different subfolders (folder structure will be 
            collapsed and goes into the filename), whereas filename will ignore 
            all similar named files after their first occurrence.
        """
        
        ## kwargs
        flag_raw_mode = raw_mode
        flag_overwrite = overwrite
        flag_resize = resize

        ## collect filepaths
        filepaths, duplicates = _file_walker(directory=image_dir, 
                                             search_mode=search_mode, 
                                             unique_mode=unique_mode, 
                                             filetypes=filetypes, 
                                             exclude=exclude, 
                                             include=include)
        
        ## feedback
        print("--------------------------------------------")
        print("phenopype will search for files at\n")
        print(image_dir)
        print("\nusing the following settings:\n")
        print("filetypes: " + str(filetypes) 
              + ", include: " + str(include)
              + ", exclude: " + str(exclude)
              + ", raw_mode: " + str(raw_mode)
              + ", search_mode: " + str(search_mode)
              + ", unique_mode: " + str(unique_mode)
              + "\n"
              )

        ## loop through files
        for filepath in filepaths:
            
            ## generate phenopype dir-tree
            relpath = os.path.relpath(filepath,image_dir)
            depth = relpath.count("\\")
            relpath_flat = os.path.dirname(relpath).replace("\\","__")
            if depth > 0:
                subfolder_prefix = str(depth) + "__" + relpath_flat + "__"
            else:
                subfolder_prefix = str(depth) + "__" 
            dirname = subfolder_prefix + os.path.splitext(os.path.basename(filepath))[0]
            dirpath = os.path.join(self.root_dir,"data",dirname)

            ## make image-specific directories
            if os.path.isdir(dirpath) and flag_overwrite==False:
                print("Found image " + relpath 
                      + " - " 
                      + dirname + " already exists (overwrite=False)")
                continue
            if os.path.isdir(dirpath) and flag_overwrite==True:
                rmtree(dirpath, ignore_errors=True, onerror=_del_rw)
                print("Found image " + relpath +
                      " - " 
                      + "phenopype-project folder " + dirname + " created (overwritten)")
                os.mkdir(dirpath)
            else:
                print("Found image " + relpath +
                      " - " 
                      + "phenopype-project folder " + dirname + " created")
                os.mkdir(dirpath)

            ## load image
            image = load_image(filepath, resize=flag_resize)
            
            ## copy or link raw files
            if flag_raw_mode == "copy":
                raw_path = os.path.join(dirpath, "raw" + os.path.splitext(os.path.basename(filepath))[1])
                if resize < 1:
                    cv2.imwrite(raw_path, image)
                else:
                    copyfile(filepath, raw_path)
            elif flag_raw_mode == "link":
                if resize < 1:
                    warnings.warn("cannot resize image in link mode")
                raw_path = filepath

            ## collect attribute-data and save
            image_data = load_image_data(filepath, flag_resize)
            meta_data = load_meta_data(filepath)
            project_data = {
                "dirname": dirname,
                "dirpath": dirpath,
                "raw_mode": flag_raw_mode,
                "raw_path": raw_path
                }
            
            if meta_data:
                attributes = {
                    "image": image_data,
                    "meta": meta_data,
                    "project": project_data}
            else:
                attributes = {
                    "image": image_data,
                    "project": project_data}

            ## write attributes file
            _save_yaml(attributes, os.path.join(dirpath, "attributes.yaml"))

            ## add to project object
            if not dirname in self.dirnames:
                self.dirnames.append(dirname)
                self.dirpaths.append(dirpath)
                self.filenames.append(image_data["filename"])
                self.filepaths.append(raw_path)
                
        print("\nFound {} files".format(len(filepaths)))
        print("--------------------------------------------")

    def add_config(self, name, preset="preset1", interactive=False, overwrite=False, 
                   **kwargs):
        """
        Add pype configuration presets to all project directories, either by using
        the templates included in the presets folder, or by adding your own templates
        by providing a path to a yaml file. Can be tested and modified using the 
        interactive flag before distributing the config files.

        Parameters
        ----------

        name: str
            name of config-file. this gets appended to all files and serves as and
            identifier of a specific analysis pipeline
        preset: str, optional
            can be either a string denoting a template name (e.g. preset1, preset2, 
            landamarking1, ... - in "phenopype/settings/presets.py") or a path to a 
            compatible yaml file
        interactive: bool, optional
            start a pype and modify preset before saving it to phenopype directories
        overwrite: bool, optional
            overwrite option, if a given pype config-file already exist
        """

        ## kwargs
        # preset = kwargs.get("preset","preset1")
        flag_interactive = interactive
        flag_overwrite = overwrite

        ## load config
        if hasattr(presets, preset):
            config = _create_generic_pype_config(preset = preset, config_name=name)
        elif os.path.isfile(preset):
            config = {"pype":{"name": name,
                              "preset": preset,
                              "date_created": datetime.today().strftime('%Y%m%d_%H%M%S')}}
            config.update(_load_yaml(preset))
            print(config)
        else:
            print("defaulting to preset " + default_pype_config)
            config = _load_yaml(eval("presets." + default_pype_config))

        ## modify
        if flag_interactive:
            image_location = os.path.join(self.root_dir,"pype_template_image" + os.path.splitext(self.filenames[0])[1])
            copyfile(self.filepaths[0], image_location)
            config_location = os.path.join(self.root_dir, "pype_config_template-" + name + ".yaml")
            _save_yaml(config, config_location)
            p = pype(image_location, name="template-" + name, config_location=config_location, presetting=True)
            config = p.config

        ## go through project directories
        for directory in self.dirpaths:
            attr = _load_yaml(os.path.join(directory, "attributes.yaml"))
            pype_preset = {"image": attr["image"]}
            pype_preset.update(config)

            ## save config
            preset_path = os.path.join(directory, "pype_config_" + name + ".yaml")
            dirname = attr["project"]["dirname"]
            if os.path.isfile(preset_path) and flag_overwrite==False:
                print("pype_" + name + ".yaml already exists in " + dirname +  " (overwrite=False)")
                continue
            elif os.path.isfile(preset_path) and flag_overwrite==True:
                print("pype_" + name + ".yaml created for " + dirname + " (overwritten)")
                _save_yaml(pype_preset, preset_path)
            else:
                print("pype_" + name + ".yaml created for " + dirname)
                _save_yaml(pype_preset, preset_path)



    def add_scale(self, template_image, **kwargs):
        """
        Add pype configuration presets to all project directories. 

        Parameters
        ----------

        template_image: str
            name of template image, either project directory or file link. template 
            image gets stored in root directory, and information appended to all 
            attributes files in the project directories
        overwrite (optional): bool (default: False)
            overwrite option, if a given pype config-file already exist
        """

        ## kwargs
        flag_overwrite = kwargs.get("overwrite", False)
        flag_template = kwargs.get("template", False)

        ## load template image
        if template_image.__class__.__name__ == "str":
            if os.path.isfile(template_image):
                template_image = cv2.imread(template_image)
            elif os.path.isdir(template_image):
                attr = _load_yaml(os.path.join(template_image, "attributes.yaml"))
                template_image = cv2.imread(attr["project"]["raw_path"])
            elif template_image in self.dirnames:
                attr = _load_yaml(os.path.join(self.data_dir, template_image, "attributes.yaml"))
                template_image = cv2.imread(attr["project"]["raw_path"])
        elif template_image.__class__.__name__ == "ndarray":
            pass
        elif template_image.__class__.__name__ == "int":
            template_image =  cv2.imread(self.filepaths[template_image])
            
        ## measure scale
        px_mm_ratio, template  = preprocessing.create_scale(template_image, template=flag_template)

        ## save template
        if not template.__class__.__name__ == "NoneType":
            template_path = os.path.join(self.root_dir, "scale_template.jpg")
            while True:
                if os.path.isfile(template_path) and flag_overwrite == False:
                    print("- scale template not saved - file already exists (overwrite=False).")
                    break
                elif os.path.isfile(template_path) and flag_overwrite == True:
                    print("- scale template saved under " + template_path + " (overwritten).")
                    pass
                elif not os.path.isfile(template_path):
                    print("- scale template saved under " + template_path + ".")
                    pass
                cv2.imwrite(template_path, template)
                break

        ## save scale information
        for directory in self.dirpaths:
            attr = _load_yaml(os.path.join(directory, "attributes.yaml"))
            if not "scale" in attr:
                print("added scale information to " + attr["project"]["dirname"])
                pass
            elif "scale" in attr and flag_overwrite:
                print("added scale information to " + attr["project"]["dirname"] + " (overwritten)")
                pass
            elif "scale" in attr and not flag_overwrite:
                print("could not add scale information to " + attr["project"]["dirname"] + " (overwrite=False)")
                continue
            attr["scale"] = {"template_path": template_path,
                             "template_px_mm_ratio": px_mm_ratio}
            _save_yaml(attr, os.path.join(directory, "attributes.yaml"))


    def save(project):
        """
        Save project to root directory
    
        Parameters
        ----------
    
        project: phenopype.main.project
            save project file to root dir of project (saves ONLY the python object needed to call file-lists, NOT collected data),
            which needs to be saved separately with the appropriate functions (e.g. "save_csv" and "save_img")
        """
        output_str = os.path.join(project.root_dir, 'project.data')
        with open(output_str, 'wb') as output:
            pickle.dump(project, output, pickle.HIGHEST_PROTOCOL)
    
    
    
    def load(path):
        """
        Load phenoype project.data file to python namespace
    
        Parameters
        ----------
    
        path: path to project.data
            load project file saved to root dir of project
        """
        with open(path, 'rb') as output:
            return pickle.load(output)



class pype:
    """
    The pype is phenopype’s core method that allows running all functions 
    that are available in the program’s library in sequence. Executing the pype routine 
    will trigger two actions: it will open a yaml configuration file 
    containing instructions for image processing using the default OS text viewer, 
    and a phenopype-window showing the image that was passed on to the pype 
    function as an array, or a character string containing the path to an 
    image on the harddrive (or a directory). Phenopype will parse all functions 
    contained in the config-file in sequence and attempt to apply them to the image 
    (exceptions will be passed, but exceptions returned for diagnostics). 
    The user immediately sees the result and can decide to make changes directly to 
    the opened config-file (e.g. either change function parameters or add new functions), 
    and run the pype again, or to terminate the pype and save all results. 
    The user can store the processed image, any extracted phenotypic information, 
    as well as the modified config-file inside the image directory. 
    By providing unique names, users can store different pype configurations and 
    the associated results side by side. 
    
    Parameters
    ----------

    image: array or str 
        can be either a numpy array or a string that provides the path to source image file 
        or path to a valid phenopype directory
    name: str
        name of pype-config - will be prepended to all results files
    config: str, optional
        chose from given presets in phenopype/settings/pype_presets.py 
        (e.g. preset1, preset2, ...)
    interactive: bool, optional
        start a pype, modify loaded preset before saving it to phenopype directories
    overwrite: bool, optional
        overwrite option, if a given pype config-file already exist
    """
    def __init__(self, image, name, config="preset1", interactive=False, overwrite=False, 
                 dirpath=None, **kwargs):

        
        ## pype name check
        if "pype_config_" in name:
            name = name.replace("pype_config_", "")
        elif ".yaml" in name:
            name = name.replace(".yaml", "")
        for char in '[@_!#$%^&*()<>?/|}{~:]\\':
            if char in name:
                sys.exit("no special characters allowed in pype name")

        ## kwargs
        flag_show = kwargs.get("show",True)
        flag_skip = kwargs.get("skip", None)
        flag_autoload = kwargs.get("autoload", True)
        flag_autosave = kwargs.get("autosave", True)
        flag_autoshow = kwargs.get("autoshow", False)

        preset = kwargs.get("preset", "preset1")
        config_location = kwargs.get("config_location", None)

        print_settings = kwargs.get("print_settings",False)
        presetting = kwargs.get("presetting", False)
        flag_meta = kwargs.get("meta", True)
        exif_fields = kwargs.get("fields", default_meta_data_fields)
        if not exif_fields.__class__.__name__ == "list":
            exif_fields = [exif_fields]

        ## load image as cointainer from array, file, or directory
        if image.__class__.__name__ == "ndarray":
            self.container = load_image(image, cont=True, meta=flag_meta)
            self.container.save_suffix = name
        elif image.__class__.__name__ == "str":
            if os.path.isfile(image):
                self.container = load_image(image, cont=True, meta=False)
                self.container.save_suffix = name
            elif os.path.isdir(image):
                self.container = load_directory(image, meta=flag_meta, fields=exif_fields)
                self.container.save_suffix = name
            else:
                sys.exit("Invalid path - cannot run pype.")
        else:
            sys.exit("Wrong input format - cannot run pype.")
        
        ## emergencycheck
        if not self.container.image or self.container.image.__class__.__name__ == "NoneType":
            sys.exit("Internal error - no image loaded.")

        ## supply dirpath manually
        if not dirpath.__class__.__name__ == "NoneType":
            self.container.dirpath = dirpath

        ## skip directories that already contain specified files
        if flag_skip:
            filepaths, duplicates = _file_walker(self.container.dirpath, 
                                                 include=flag_skip, 
                                                 exclude=["pype_config"], 
                                                 pype_mode=True)
            if len(filepaths)>0:
                print("\nskipped\n")
                return

        ## load config
        if config_location:
            self.config, self.config_location = _load_pype_config(config_location)
        else:
            self.config, self.config_location = _load_pype_config(self.container, config_name=name, preset=preset)

        ## open config file with system viewer
        if flag_show:
            if platform.system() == 'Darwin':       # macOS
                subprocess.call(('open', self.config_location))
            elif platform.system() == 'Windows':    # Windows
                os.startfile(self.config_location)
            else:                                   # linux variants
                subprocess.call(('xdg-open', self.config_location))

        ## initialize
        self.FM = _yaml_file_monitor(self.config_location, print_settings=print_settings)
        update, iv = {}, None
        
        # =============================================================================
        # pype
        # =============================================================================
        
        while True:

            ## get config file and assemble pype
            self.config = copy.deepcopy(self.FM.content)
            if not self.config:
                continue

            ## feedback
            print("\n\n------------+++ new pype iteration " + 
                  datetime.today().strftime('%Y:%m:%d %H:%M:%S') + 
                  " +++--------------\n\n")

            # reset values            
            self.container.reset()
            if flag_autoload:
                self.container.load()
            restart = None
            export_list, show_list = [], []

            ## apply pype
            for step in list(self.config.keys()):
                if step in ["image", "meta", "pype"]:
                    continue
                if not self.config[step]:
                    continue
                if step == "export" and presetting == True:
                    continue
                print(step.upper())
                for item in self.config[step]:
                    try:

                        ## construct method name and arguments
                        if item.__class__.__name__ == "str":
                            method_name = item
                            method_args = {}
                        elif item.__class__.__name__ == "CommentedMap":
                            method_name = list(item)[0]
                            if not list(dict(item).values())[0]:
                                method_args = {}
                            else:
                                method_args = dict(list(dict(item).values())[0])

                        ## collect save-calls
                        if step == "export":
                            export_list.append(method_name)
                            
                        elif step == "visualization":
                            show_list.append(method_name)

                        ## run method
                        print(method_name)
                        method_loaded = eval(step + "." + method_name)
                        restart = method_loaded(self.container, **method_args)
                        
                        ## control
                        if restart:
                            print("RESTART")
                            break
                        
                    except Exception as ex:
                        location = step + "." + method_name + ": " + str(ex.__class__.__name__)
                        print(location + " - " + str(ex))
                        
                if restart:
                    break
            if restart:
                continue

            # save container 
            if flag_autoshow:
                self.container.show(show_list=show_list)
            if not presetting:
                if flag_autosave:
                    self.container.save(export_list=export_list)

            ## visualize output
            try:
                if not "visualization" in list(self.config.keys()):
                    print("select")
                    visualization.select_canvas(self.container)
                iv = _image_viewer(self.container.canvas, previous=update)
                update = iv.__dict__
            except Exception as ex:
                print("visualisation: " + str(ex.__class__.__name__) + " - " + str(ex))

            ## terminate
            if iv:
                if iv.done:
                    self.FM.stop()
                    print("\n\nTERMINATE")
                    break