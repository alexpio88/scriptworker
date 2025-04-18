#===============================================
# Runic Tools Combiner
#===============================================
# Author       : TheWolf
# Release Nr   : 00
# Release Date : April 04, 2024
#===============================================
# Tested on
#===============================================
# Razor Version : 0.8.2.120
# Server        : login.uodreams.com
# UO Version    : 7.0.98
#===============================================
# What you need:
#  Imbuing skill >= 65
#  Soulforge
#  Runic Tools
#===============================================
# Description:
#  Keep runic tools in backpack or in a container
#  inside backpack.
#  Target the runic tools container.
#  Target the runic tools you want to combine. 
#  Merge all tools not exceed 100 charges.

from System.Collections.Generic import List
from System import Byte, Int32


class ip: #item properties
    def __init__(self,ID,Hue):
        self.ID = ID
        self.Hue = Hue
        
itemDic = {
'dull copper runic hammer' : ip(0x13E3,0x0973),
'shadow runic hammer'      : ip(0x13E3,0x0966),
'copper runic hammer'      : ip(0x13E3,0x096d),
'bronze runic hammer'      : ip(0x13E3,0x0972),
'golden runic hammer'      : ip(0x13E3,0x08a5),
'agapite runic hammer'     : ip(0x13E3,0x0979),
'verite runic hammer'      : ip(0x13E3,0x089f),
'valorite runic hammer'    : ip(0x13E3,0x08ab),
'spined leather runic sewing kit' : ip(0x0F9D,0x08ac),
'horned leather runic sewing kit' : ip(0x0F9D,0x0845),
'barbed leather runic sewing kit' : ip(0x0F9D,0x0851),
'Oak Runic Fletcher\'s Tools'       : ip(0x1022,0x07da),
'Ash Runic Fletcher\'s Tools'       : ip(0x1022,0x04a7),
'Yew Runic Fletcher\'s Tools'       : ip(0x1022,0x04a8),
'Heartwood Runic Fletcher\'s Tools' : ip(0x1022,0x04a9),
'Dull Copper Runic Mallet and Chisels' : ip(0x12B3,0x0973),
'Shadow Runic Mallet and Chisels'      : ip(0x12B3,0x0966),
'Copper Runic Mallet and Chisels'      : ip(0x12B3,0x096d),
'Bronze Runic Mallet and Chisels'      : ip(0x12B3,0x0972),
'Golden Runic Mallet and Chisels'      : ip(0x12B3,0x08a5),
'Agapite Runic Mallet and Chisels'     : ip(0x12B3,0x0979),
'Verite Runic Mallet and Chisels'      : ip(0x12B3,0x089f),
'Valorite Runic Mallet and Chisels'    : ip(0x12B3,0x08ab),
'Oak Runic Dovetail Saw'       : ip(0x1028,0x07da),
'Ash Runic Dovetail Saw'       : ip(0x1028,0x04a7),
'Yew Runic Dovetail Saw'       : ip(0x1028,0x04a8),
'Heartwood Runic Dovetail Saw' : ip(0x1028,0x04a9),
}

soulforgeIDdic = {
0x2DD8 : 'Minion Soulforge',
0x4286 : 'Soulforge',
0x426D : 'Queen\'s Forge'
}

def checkSoulforge():
    fil = Items.Filter()
    fil.Enabled = True
    fil.RangeMax = 2
    fil.Graphics = List[Int32](list(soulforgeIDdic.keys()))
    itemsFound = Items.ApplyFilter(fil)
    if len(itemsFound) > 0 : return True
    else : 
        Player.HeadMessage(60,'Soulforge missing or too far')
        return False
        
def combineTool(toolSerialList):
    getPropValueItem1 = Items.GetPropValue(toolSerialList[0],'Uses Remaining')
    for i in range(1,len(toolSerialList)):
        getPropValueItem2 = Items.GetPropValue(toolSerialList[i],'Uses Remaining')
        if getPropValueItem1 + getPropValueItem2 <= 100 :
            Items.UseItem(Items.FindBySerial(toolSerialList[0]))
            Target.WaitForTarget(10000, False)
            Target.TargetExecute(Items.FindBySerial(toolSerialList[i]))
            Misc.Pause(250)
            toolSerialList.pop(i)
            combineTool(toolSerialList)
            break
    if len(toolSerialList) > 2 : 
        toolSerialList.pop(0)
        combineTool(toolSerialList)
        
def countTools(serialContainer):
    serialListDic = dict()
    for k,v in itemDic.items():
        for item in Items.FindBySerial(serialContainer).Contains :
            if v.ID == item.ItemID and v.Hue == item.Hue:
                if k in serialListDic: serialListDic[k] += [item.Serial]
                else : serialListDic[k] = [item.Serial]
    return serialListDic
    
if Player.GetSkillValue('Imbuing') >= 65:
    if checkSoulforge():
        serialContainer = Target.PromptTarget('target container',55)
        Items.WaitForContents(serialContainer,5000)
        tools = countTools(serialContainer)
        for k,v in tools.items():
            if len(v) > 1 : combineTool(v)
else : Player.HeadMessage(55,'You need imbuing >= 65')
