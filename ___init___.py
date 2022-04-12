# virtualenv venv
#source venv/bin/activate
#folder_exists
import io
import os

#import octoprint.filemanager
import octoprint.filemanager.storage

#import octoprint.plugin
from octoprint.filemanager.destinations import FileDestinations
from octoprint.filemanager.util import StreamWrapper


class HelloWorldPlugin(octoprint.plugin.StartupPlugin,
                       octoprint.plugin.TemplatePlugin,
                       octoprint.plugin.SettingsPlugin,
                       octoprint.plugin.AssetPlugin):
        # **Icon
        # **Revision 
        # ***add configure may for Que addon 
        # *own addon for configre jyers
        # Get all FileNames  -> check :D
        # Map and add Command -> on thinging stage -> duple [name, printCommand,May Icons] -> check :D 
        # *cleanUp 
        # make local Files -> check:
        #git commit
        # write to File 
        # make own Gcommands
        # make file with own Gcode -> add to File 
                                    #Gcode if octopi is not listinong
                                    #Gcode wait
                                    # let octoPrint print files 
        # * manipulate add delete *Folder
        #  Hook into:  OR ONLY FOR BOOT Or Only by update Command ? 
            # rename
            # delete
            # uploud
            # folder
        # Send Map 
        #
        # C++ add Folder 
        # C++ send Command
        # C++ 
        # C++ Make Confuigure 
        # Recive 
        #  Print 
    def on_after_startup(self):
        
        Filemanager = octoprint.filemanager.storage.LocalFileStorage(
            self.get_plugin_data_folder()
        )

        #breakpoint()
        print('\x1b[6;30;42m' + 'Spacer--------______________________________!' + '\x1b[0m')
        files = self._file_manager.list_files(FileDestinations.LOCAL)
        fileNameList = [*files.get('local').keys()]
        #filenames = dictFilenames() ## should remove dict
        self._logger.info(fileNameList)
        fileNameDict = dict(file0 = {'filename': 'examplename', 'command': 'example40001', 'icon': 'shouldbeimplemented'})
        for itr, fileName in enumerate(fileNameList):
            strCounter = str(itr)
            fileNameDict['file' + strCounter] = {'filename': fileName, 'command': 'example4000' + strCounter, 'icon': 'shouldbeimplemented'}
        fileNameDict.pop('file0')

        #self._logger.info(fileNameDict)
        #list done  #make Folder
        path = self.get_plugin_data_folder() +"/readyFiles"
        self._logger.info(path)
        if not Filemanager.folder_exists(path):
            print('\x1b[6;30;42m' + 'in if :D' + '\x1b[0m')
            Filemanager.add_folder(path)
        
        #add Files
        file_obj = StreamWrapper(
            os.path.basename(path),
            io.BytesIO(
                ";Generated from kil\n".format(
                    **locals()
                ).encode("ascii", "replace")
            )
        )
        for fId, fItem in fileNameDict.items():
            pathWithFile = path + '/' +fItem['filename']
            if not Filemanager.file_exists(pathWithFile):
                Filemanager.add_file(pathWithFile, file_object=file_obj,  allow_overwrite=False, display=None)
                print('\x1b[6;30;42m' + fId + ' wrote'+ '\x1b[0m')

        print('\x1b[6;30;42m' + "done" + '\x1b[0m')
 
    def get_settings_defaults(self):
        return dict(url="https://en.wikipedia.org/wiki/Hello_world")


    def get_template_configs(self):
        for _ in range(10):
            self._logger.info("Hello World! (more: %s)" % self._settings.get(["url"]))
        print('\x1b[6;30;42m' + 'Spacer--------______________________________!' + '\x1b[0m')


        return [
            dict(type="navbar", custom_bindings=False),
            dict(type="settings", custom_bindings=False)
        ]

__plugin_name__ = "Hello World"
__plugin_version__ = "1.0.0"
__plugin_description__ = "A quick \"Hello World\" example plugin for OctoPrint"
__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_implementation__ = HelloWorldPlugin()
