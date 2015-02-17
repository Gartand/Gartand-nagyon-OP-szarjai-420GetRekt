# coding=utf-8
__author__ = 'Gartand'
__version__ = '1.1'


import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite

blue = "[color #0099FF]"
red = "[color #FF0000]"
pink = "[color #CC66FF]"
teal = "[color #00FFFF]"
green = "[color #009900]"

class Report:

    def On_PluginInit(self):
        self.IniFile()

    def argsToText(self, args):
        text = str.join(" ", args)
        return text

    def isMod(self, id):
        if DataStore.ContainsKey("Moderators", id):
            return True
        return False

    def IniFile(self):
        if not Plugin.IniExists("ReportedPlayers"):
            ini = Plugin.CreateIni("ReportedPlayers")
            ini.Save()
        return Plugin.GetIni("ReportedPlayers")

    """
        CheckV method based on Spock's method.
        Upgraded by DreTaX
        Can Handle Single argument and Array args.
        V4.1
    """

    def GetPlayerName(self, namee):
        try:
            name = namee.lower()
            for pl in Server.Players:
                if pl.Name.lower() == name:
                    return pl
            return None
        except:
            return None

    def CheckV(self, Player, args):
        systemname = "Report"
        count = 0
        if hasattr(args, '__len__') and (not isinstance(args, str)):
            p = self.GetPlayerName(str.join(" ", args))
            if p is not None:
                return p
            for pl in Server.Players:
                for namePart in args:
                    if namePart.lower() in pl.Name.lower():
                        p = pl
                        count += 1
                        continue
        else:
            nargs = str(args).lower()
            p = self.GetPlayerName(nargs)
            if p is not None:
                return p
            for pl in Server.Players:
                if nargs in pl.Name.lower():
                    p = pl
                    count += 1
                    continue
        if count == 0:
            Player.MessageFrom(systemname, "Couldn't find [color#00FF00]" + str.join(" ", args) + "[/color]!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.MessageFrom(systemname, "Found [color#FF0000]" + str(count) + "[/color] player with similar name. [color#FF0000] Use more correct name!")
            return None

    def SaveReportToIni(self, Reporter, ReportedName, Text):
        ini = self.IniFile()
        enum = ini.EnumSection("Reports")
        length = len(enum)
        lastreportnumber = 0
        for number in xrange(0, length + 1):
            if number == length:
                lastreportnumber = enum[number]
        ini.AddSetting("Reports", str(lastreportnumber + 1), "| Reporter: " + Reporter.Name+" -| Reported:  " + ReportedName + " -| Reason: " + Text)
        ini.Save()

    def On_Command(self, Reporter, cmd, args):
        ini = self.IniFile()
        enum = ini.EnumSection("Reports")
        length = len(enum)
        if cmd == "report":
            if len(args) == 0:
                Reporter.MessageFrom("Report", green + "Get420Reported++ " + __version__ + " Made by " + __author__)
                Reporter.MessageFrom("Report", "/report Name")
                Reporter.MessageFrom("Report", "/report list")
                Reporter.MessageFrom("Report", "/report delete")
                Reporter.MessageFrom("Report", "/report deleteall")
            else:
                if args[0] == "help":
                    Reporter.MessageFrom("Report", green + "Get420Reported++ " + __version__ + " Made by " + __author__)
                    Reporter.MessageFrom("Report", "/report Name")
                    Reporter.MessageFrom("Report", "/report list")
                    Reporter.MessageFrom("Report", "/report delete")
                    Reporter.MessageFrom("Report", "/report deleteall")
                elif args[0] == "list":
                    if not Reporter.Admin and not self.isMod(Reporter.SteamID):
                        return
                    Reporter.MessageFrom("Report", green + "There are (" + teal + str(length) + green + ") reports atm.")
                    for key in enum:
                        Reporter.MessageFrom("Report", "ID - " + key)
                elif args[0] == "view":
                    if not Reporter.Admin and not self.isMod(Reporter.SteamID):
                        return
                    # cmd args[0] args[1]
                    # /report view id
                    if len(args) == 1:
                        Reporter.MessageFrom("Report", red + "Usage: /report view id")
                        return
                    id = args[1]
                    if not id.isdigit():
                        Reporter.MessageFrom("Report", red + "ID must be a number.")
                        return
                    if not ini.GetSetting("Reports", id) and ini.GetSetting("Reports", id) is None:
                        Reporter.MessageFrom("Report", red + "This report doesn't exist!")
                        return
                    Reason = ini.GetSetting("Reports", id)
                    Reporter.MessageFrom("Report", red + "You are viewing: " + id)
                    Reporter.MessageFrom("Report", green + "Case: " + teal + Reason)
                elif args[0] == "delete":
                    if not Reporter.Admin and not self.isMod(Reporter.SteamID):
                        return
                    if len(args) == 1:
                        Reporter.MessageFrom("Report", red + "Usage: /report delete id")
                        return
                    id = args[1]
                    if not id.isdigit():
                        Reporter.MessageFrom("Report", red + "ID must be a number.")
                        return
                    ini.DeleteSetting("Reports", id)
                    Reporter.MessageFrom("Report", red + "Case:" + id + " deleted.")
                    ini.Save()
                elif args[0] == "deleteall":
                    if not Reporter.Admin and not self.isMod(Reporter.SteamID):
                        return
                    for key in enum:
                        ini.DeleteSetting("Reports", key)
                    Reporter.MessageFrom("Report", red + "All cases deleted.")
                    ini.Save()
                else:
                    Reported = self.CheckV(Reporter, args)
                    if Reported is None:
                        return
                    if DataStore.ContainsKey("Report", Reporter.SteamID):
                        Reporter.MessageFrom("Report", red + "Write the reason in the chat without the command.")
                        return
                    Reporter.MessageFrom("Report", red + "Write the reason in the chat.")
                    # Tábla, Kulcs, Érték
                    # Tábla, Reportoló játékos id, Reportolt játékos id-t
                    DataStore.Add("Report", Reporter.SteamID, Reported.SteamID)
                    DataStore.Add("Report", Reporter.SteamID + "name", Reported.Name)

    def On_Chat(self, Reporter, ChatMessage):
        if DataStore.ContainsKey("Report", Reporter.SteamID):
            message = ChatMessage.ToString()
            ChatMessage.NewText = ""
            if len(message) > 47:
                Reporter.MessageFrom("Report", red + "Too long reason. Write It shorter.")
                return
            SteamID = DataStore.Get("Report", Reporter.SteamID)
            Name = DataStore.Get("Report", Reporter.SteamID + "name")
            #Keresett Jatekos
            for player in Server.Players:
                if player.Admin or self.isMod(player.SteamID):
                    player.MessageFrom("Report", red + "New report submitted!")
                    player.MessageFrom("Report", red + "Check it with the /report view command.")
            DataStore.Remove("Report", Reporter.SteamID)
            Plugin.Log("ReportLogs", "Reporter: " + Reporter.Name + " | " + Reporter.SteamID + " | Reported: " + Name +
                       " | " + SteamID + " |  Reason: " + message)
            self.SaveReportToIni(Reporter, Name, message)
            Reporter.MessageFrom("Report", red + "Report submitted.")