# coding=utf-8
__author__ = 'Garrus'
__version__ = '1.0'


import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite

red = "[color #FF0000]"

class Report:

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

    def On_Command(self, Reporter, cmd, args):
        if cmd == "report":
            Reported = self.CheckV(Reporter, args)
            if Reported is None:
                return
            if DataStore.ContainsKey("Report", Reporter.SteamID):
                Reporter.MessageFrom("Report", red + "Write the reason in the chat without the command.")
                return
            Reporter.MessageFrom("Report", "Write the reason in the chat.")
            # Tábla, Kulcs, Érték
            # Tábla, Reportoló játékos id, Reportolt játékos id-t
            DataStore.Add("Report", Reporter.SteamID, Reported.SteamID)
            DataStore.Add("Report", Reporter.SteamID + "name", Reported.Name)

    def On_Chat(self, Reporter, Text):
        if DataStore.ContainsKey("Report", Reporter.SteamID):
            SteamID = DataStore.Get("Report", Reporter.SteamID)
            Name = DataStore.Get("Report", Reporter.SteamID + "name")
            #Keresett Jatekos
            for player in Server.Players:
                if player.Admin or self.isMod(player.SteamID):
                    # BizonyosJatekos.Uzenet
                    player.MessageFrom("Report", Text)
            DataStore.Remove("Report", Reporter.SteamID)
            Plugin.Log("ReportLogs", Name + " | " + SteamID + " | " + Text)
            Text = ""