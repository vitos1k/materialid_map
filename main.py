import bpy
from random import randint,seed
maxim = len(bpy.data.materials)


def ranomizelist(sed = None):
    seed(sed)
    randlist = []
    countlist = [x for x in range(maxim)]
    for k in range(maxim):
        temp_pos = randint(0,len(countlist)-1)
        temp_val = countlist[temp_pos]
        randlist.append(temp_val)
        countlist.pop(temp_pos)
    print(randlist)
    return randlist
        
def create_ids(material):
    nodes = material.node_tree.nodes
    co = (0,0)
    for node in nodes:
        if node.type == 'OUTPUT_MATERIAL':
            co = node.location
            
    
    group_node = nodes.new("ShaderNodeGroup")
    group_node.location = co
    group_node.location[1] -= 125
    group_node.node_tree = bpy.data.node_groups['MAT_ID_GROUP']
   

def create_group():
    group = bpy.data.node_groups.new(type="ShaderNodeTree", name="MAT_ID_GROUP")
     # add Object Info node
    first_node = group.nodes.new(type="ShaderNodeObjectInfo")
    first_node.name = 'IDMAP_ObjectInfo'
    first_node.location = (0,0)
    
    #add math node
    second_node = group.nodes.new(type="ShaderNodeMath")
    second_node.name = 'IDMAP_Math'
    second_node.operation = 'DIVIDE'
    second_node.location = (200,-150)
    
    #add Value node
    third_node = group.nodes.new(type='ShaderNodeValue')
    third_node.name = 'IDMAP_Value'
    third_node.outputs[0].default_value = maxim
    third_node.location = (0,-300)
    
    #add colorramp node
    fourth_node = group.nodes.new(type="ShaderNodeValToRGB")
    fourth_node.name = "IDMAP_ValToRGB"
    fourth_node.color_ramp.elements[0].color = (0, 0, 1, 1)
    fourth_node.color_ramp.elements[0].position = 0.0
    fourth_node.color_ramp.elements[1].color = (0, 0, 1, 1)
    fourth_node.color_ramp.elements[1].position = 1.0
    fourth_node.color_ramp.color_mode = 'HSL'
    fourth_node.color_ramp.hue_interpolation = 'FAR'
    fourth_node.location = (400,-100)
    
    #add AOV node
    fifth_node = group.nodes.new(type="ShaderNodeOutputAOV")
    fifth_node.name = "MatID"
    fifth_node.location = (800,-75)

        
    # connect nodes
    group.links.new(second_node.inputs[0] ,first_node.outputs[3])
    group.links.new(second_node.inputs[1] ,third_node.outputs[0])
    group.links.new(fourth_node.inputs[0],second_node.outputs[0])
    group.links.new(fifth_node.inputs[0], fourth_node.outputs[0])

def update_group():
    bpy.data.node_groups['MAT_ID_GROUP'].nodes['IDMAP_Value'].outputs[0].default_value = maxim


if __name__ == "__main__":
    #check fi group exists
    no_group = True
    for group in bpy.data.node_groups:
        if group.name=="MAT_ID_GROUP":
            no_group = False
    if no_group:
        create_group()
    else:
        update_group()
               
    #check if AOV is exists
    # if no AOV in 
    no_aov = True
    if 'aovs' in bpy.context.view_layer.cycles.keys():
        aovs = [aov.to_dict() for aov in bpy.context.view_layer.cycles['aovs']]
        for aov_name in aovs:
            if aov_name['name'] == 'MatID':
                no_aov = False
    if no_aov:
        bpy.ops.cycles.add_aov()
        aovs = [aov.values() for aov in bpy.context.view_layer.cycles['aovs']]
        bpy.context.view_layer.cycles['aovs'][len(aovs)-1].update({'name':'MatID','conflict': '', 'type': 1})
        
        
    ###########################################################RANDOM SEED###################################################
        
    set_seed = 0    
    
    #########################################################################################################################    
    
    valuelist = ranomizelist(set_seed)
    for i,mat in enumerate(bpy.data.materials):
        mat.pass_index = valuelist[i]
        if mat.use_nodes:
            id_created = False
            for node in mat.node_tree.nodes:
                if node.type == 'GROUP':
                    if node.node_tree.name_full == 'MAT_ID_GROUP':
                        id_created = True
            if (not (id_created)):
                create_ids(mat)
