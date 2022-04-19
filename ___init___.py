# virtualenv venv
#source venv/bin/activate
#folder_exists
import io
import os
import sys
import time
from mimetypes import init
from multiprocessing.connection import wait
from operator import contains
from pickle import TRUE

#import octoprint.filemanager
import octoprint.filemanager.storage
import octoprint.printer

#import octoprint.plugin
from octoprint.filemanager.destinations import FileDestinations
from octoprint.filemanager.util import StreamWrapper
from octoprint.server import printer

__plugin_name__ = "Action Commands"
__plugin_version__ = "0.5"
__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_description__ = "A quick \"Hello World\" example plugin for OctoPrint"

def __plugin_load__():
    global _plugin
    global __plugin_hooks__
    global gFileNameDict 
    global gCounter
    gFileNameDict = dict()
    gCounter = 1
    global __plugin_implementation__
    __plugin_implementation__ = HelloWorldPlugin()
    
    __plugin_hooks__ = {
        "octoprint.comm.protocol.action": __plugin_implementation__.hook_actioncommands 
       # "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }



class HelloWorldPlugin(octoprint.plugin.StartupPlugin,
                       octoprint.plugin.TemplatePlugin,
                       octoprint.plugin.SettingsPlugin,
                       octoprint.plugin.AssetPlugin):

        # Get all FileNames  -> check :D
        # Map and add Command -> on thinging stage -> duple [name, printCommand,May Icons] -> check :D 
        # *cleanUp 
        # make local Files -> check:
        #git commit -> zwischencheck 
        # write to File -> check c:
        # make own Gcommands -> donne 
        # get all with Foldercrap -.- check origin codde
        # Bad Info aufbohren for list Files Funcion -> FUUUUUUUUUUUUUUUUUUUUUUUUUUUCK DONE
        # make file with own Gcode -> add to File  -> done 
                                    # let octoPrint print files -> done
                                    # add update for bugs 
        # **Icon
        # **Revision 
        # ***add configure may for Que addon 
        # *own addon for configre jyers
        #  Hook into:  OR ONLY FOR BOOT Or Only by update Command ? 
            # rename
            # delete
            # uploud
            # folder FUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUuCK 
        # Send Map 


        # implement trigger       def add_sd_file( self, filename, path, on_success=None, on_failure=None, *args, **kwargs):
        # https://docs.octoprint.org/en/master/plugins/hooks.html#octoprint-comm-protocol-action
        #https://github.com/benlye/OctoPrint-ActionCommandsPlugin/blob/aba2ade9c1116c655bf3e61d3ed4696b6be2ddcb/octoprint_actioncommands/__init__.py#L94
        #| Sends a custom "// action:<action> <parameters>"
        #| Sends a custom "// action:<action> <parameters>"
    def __init__(self):
        self.customFolderName = ""
        
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


    def hook_actioncommands(self, comm, line, command, *args, **kwargs):
        self._logger.info("Command received: 'action:%s'" % (command))
        
        if command == None or not "startProntFromOctoPrint" in command:
            return

        else:
            self._logger.info("StartCommand found for 'action:%s'" % (command))
            #add get_state_string  https://docs.octoprint.org/en/master/modules/printer.html?highlight=print#
            if self._printer.is_ready():
                #(path, sd, printAfterSelect=False, pos=None, tags=None, *args, **kwargs)¶
                self._printer.unselect_file()
                try:
                   # self._printer.select_file( ,False , True,  )
                    self._logger.info("StartCommand found for 'action:%s'" % (command))

              #  except InvalidFileLocation:
               #     self._logger.info("StartCommand found for 'action:%s'" % (command))
                    #try new List
                except:
                    print("Something else went wrong") 
                #self._printer.start_print()

    
    def checkDict(self, dict):
        for key, subNode in dict.items():
            if subNode["type"] == "folder":
                self.checkDict(subNode["children"])
            else:
                self.addToDict(subNode)

    def getLocalFilesDict(self): # add Filter or mapping 
        global  gFileNameDict
        files = (self._file_manager.list_files(FileDestinations.LOCAL, recursive=True, force_refresh=True))['local']
        #filenames = dictFilenames() ## should remove dict
        self._logger.info(files)
        #self._logger.info(fileNameList)
        gFileNameDict['file0'] = {'filename': 'examplename', 'path': 'some_folder/some_file.gcode', 'icon': 'shouldbeimplemented'}
        self.checkDict(files)
        gFileNameDict.pop('file0')
        self._logger.info(gFileNameDict)
        return gFileNameDict

    def addToDict(self,node):
        global gCounter
        global  gFileNameDict
        test = str(gCounter)
        gFileNameDict['file' + test] = {'filename': node['name'], 'path': node['path'] , 'icon': 'shouldbeimplemented'}
        #gFileNameDict['file' + str(gCounter)] = {'filename': node['name'], 'path': node['path'] , 'icon': 'shouldbeimplemented'}
        gCounter = gCounter + 1  
            
    def on_after_startup(self):
        
        plugin = HelloWorldPlugin()
        Filemanager = octoprint.filemanager.storage.LocalFileStorage(
            self.get_plugin_data_folder()
        )
        #printer = Printer(Filemanager, analysisQueue, printerProfileManager)
        #breakpoint()
        print('\x1b[6;30;42m' + 'Spacer--------______________________________!' + '\x1b[0m')
        fileNameDict = self.getLocalFilesDict()
        #self._logger.info(fileNameDict)
        #list done  #make Folder
        path = self.get_plugin_data_folder() +"/readyFiles"
        self._logger.info(path)
        self._logger.info(self)
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
            fileName = fItem['filename']
            pathWithFile = path + '/' + fileName
            if not Filemanager.file_exists(pathWithFile):
                Filemanager.add_file(pathWithFile, file_object=file_obj,  allow_overwrite=False, display=None)
                file = open(pathWithFile, "w")
                file.write("M118 A1 action:startPrintFromOctoPrint '" + fItem['path']+ "'")
                file.close()
                print('\x1b[6;30;42m' + fId + ' wrote'+ '\x1b[0m')
            # add config Folder to fileName HERE !    
            #self._printer.add_sd_file(fileName, pathWithFile, tags={"source:api", "api:files.sd"} ) <- working but not on virtualPrinter

        #time.sleep(5)
        #https://docs.octoprint.org/en/master/plugins/hooks.html?highlight=sd#sd_card_upload_hook sd_card_upload_hook
        print('\x1b[6;30;42m' + 'wait done' + '\x1b[0m')
        #lol = self._file_manager.list_files(FileDestinations.SDCARD)
        #self._logger.info(lol)
        print('\x1b[6;30;42m' + "done" + '\x1b[0m')
        # code write files            

#                file.write("M118 A1 action:startProntFromOctoPrint " + fileName)

        # if this_command["type"] == "gcode":
        #     self._logger.info("Command 'action:%s' is type 'gcode'" % (command))
        #     self._logger.info("Executing printer command '%s'" % (this_command["command"]))
        #     self._printer.commands(this_command["command"].split(";"))

        # elif this_command["type"] == "system":
        #     self._logger.info("Command 'action:%s' is type 'system'" % (command))
        #     self._logger.info("Executing system command '%s'" % (this_command["command"]))

        #     try:
        #         r = os.system(this_command["command"])
        #     except:
        #         e = sys.exc_info()[0]
        #         self._logger.exception("Error executing command '%s'" % (this_command["command"]))
        #         return (None,)
            
        #     self._logger.info("Command '%s' returned: %s" % (this_command["command"], r))
            
        # else:
        #     self._logger.error("Command type not found or not known for 'action:%s'" % command)
        #     return (None,)    
 
