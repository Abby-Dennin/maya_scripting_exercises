from maya import cmds
from MayaUI import BaseWindow


def tween(percentage, obj=None, attrs=None, selection=True):                                            
    """                                                                                                 
    This function will tween the keyed attributes on an object                                          
    with the given percentage.                                                                          
    Args:                                                                                               
        percentage: the percentage for the tween                                                        
        obj: the object being keyed                                                                     
        attrs: list of the attributes to tween                                                          
        selection: whether to use selection or not                                                      
    """                                                                                                 
    if not obj and not selection:                                                                       
        raise ValueError("No object given to tween")                                                    
                                                                                                        
    if not obj:                                                                                         
        obj = cmds.ls(selection=True)[0]                                                                
                                                                                                        
    if not attrs:                                                                                       
        attrs = cmds.listAttr(obj, keyable=True)                                                        
                                                                                                        
    current_time = cmds.currentTime(query=True)                                                         
                                                                                                        
    for attr in attrs:                                                                                  
        attr_full = '%s.%s' % (obj, attr)                                                               
        keyframes = cmds.keyframe(attr_full, query=True)                                                
                                                                                                        
        if not keyframes:                                                                               
            continue                                                                                    
                                                                                                        
        past_keyframes = [frame for frame in keyframes if frame < current_time]                         
        future_keyframes = [frame for frame in keyframes if frame > current_time]                       
                                                                                                        
        if not past_keyframes and not future_keyframes:                                                 
            continue                                                                                    
                                                                                                        
        previous_frame = max(past_keyframes) if past_keyframes else None                                
        next_frame = min(future_keyframes) if future_keyframes else None                                
                                                                                                        
        if not previous_frame or not next_frame:                                                        
            continue                                                                                    
                                                                                                        
        previous_value = cmds.getAttr(attr_full, time=previous_frame)                                   
        next_value = cmds.getAttr(attr_full, time=next_frame)                                           
                                                                                                        
        difference = next_value - previous_value                                                        
                                                                                                        
        weighted_difference = (difference * percentage) / 100.0                                         
        current_value = previous_value + weighted_difference                                            
                                                                                                        
        cmds.setKeyframe(attr_full, time=current_time, value=current_value)                             
                                                                                                        
                                                                                                        
class TweenWindow(BaseWindow):                                                                              
    """                                                                                                 
    This class builds a window for the tween function.                                                  
    """                                                                                                 
    def __init__(self):                                                                                 
        self.slider = None                                                                              
        self.window_name = "TweenerWindow"                                                                                                                                           
                                                                                                        
    def build(self):                                                                                    
        column = cmds.columnLayout()                                                                    
        cmds.text(label="Use this slider to set the tween amount")                                      
        row = cmds.rowLayout(numberOfColumns=2)                                                         
        self.slider = cmds.floatSlider(min=0, max=100, value=50, step=1, changeCommand=tween)           
        cmds.button(label="Reset", command=self.reset)                                                  
                                                                                                        
        cmds.setParent(column)                                                                          
        cmds.button(label="Close", command=self.close)                                                  
                                                                                                        
    def reset(self, *args):                                                                             
        cmds.floatSlider(self.slider, edit=True, value=50)                                                                                                               
                                                                                                        
                                                                                                        
                                                                                                        