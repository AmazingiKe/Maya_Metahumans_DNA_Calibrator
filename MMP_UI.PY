"""
插件名字全程叫 >>> Metahumans DNA calibrator

docs
https://github.com/revoconner/metahuman_rig_transfer

"""
#---------------------------------------------------------------

# Maya库导入
from maya import cmds
import maya.OpenMayaUI as omui
import maya.mel as mel

# PySide2
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
from shiboken2 import wrapInstance

# python自带的库
import os
import sys
import importlib
import re

# 导入其他库
Script_path = os.path.join(os.path.dirname(__file__))
External_library_path = Script_path + '\\' + 'External_library'
sys.path.append(External_library_path)

# 图标路径
icon_path = Script_path +'\\icon\\'

# 导入我的库
import Metahuman_edit_tool as DNA_ET
importlib.reload(DNA_ET)

import Data_storage_module as DSM
importlib.reload(DSM)

#---------------------------------------------------------------

def maya_main_window():
	"""获取maya主窗口"""
	main_window_ptr = omui.MQtUtil.mainWindow()
	return wrapInstance(int(main_window_ptr),QtWidgets.QWidget)



class MMP_MAIN_UI(QtWidgets.QDialog):
	
	WIN_NAME = "MMP_WIN"
	TITLE = 'Metahuman Multipurpose Tool V0.6.1 --Amazing_iKe'
	
	def __init__(self,parent = maya_main_window()):
		
		super(MMP_MAIN_UI, self).__init__(parent)
		
		
		if cmds.window(MMP_MAIN_UI.WIN_NAME, exists=True):
			cmds.deleteUI(MMP_MAIN_UI.WIN_NAME)
			
			
		#...窗口名字
		self.setObjectName(MMP_MAIN_UI.WIN_NAME)
		self.setWindowTitle(MMP_MAIN_UI.TITLE)

		#...窗口长宽
		self.setMinimumHeight(200)
		self.setMinimumWidth(600)
		
		self.create_widgets()
		self.create_layouts()
		
	def create_widgets(self,):

		# 创建一个菜单栏
		self.menu_bar = QtWidgets.QMenuBar(self)


		self.optimize_menu_item = self.menu_bar.addMenu('基础DNA工具')
		self.optimize_menu_item.addAction('处理Bridge身体', self.body_processing_win)
		self.optimize_menu_item.addAction('计算较低 LOD 网格', self.calculate_lower_lod_mesh_win)
		self.optimize_menu_item.addAction('删除DNA BS', self.dna_clear_blend_shapes_win)
		self.optimize_menu_item.addAction('获取DNA所有信息', self.dna_data_dict_win)
		self.optimize_menu_item.addAction('转JSON', self.dna_binary_to_json_win)
  
		self.optimize_menu_item = self.menu_bar.addMenu('高级DNA工具')
		self.optimize_menu_item.addAction('设置Descriptor层', self.descriptor_modify_win)
  
		self.optimize_menu_item = self.menu_bar.addMenu('优化')
		self.optimize_menu_item.addAction('优化场景', self.optimize_dna_scene_win)

		self.optimize_menu_item = self.menu_bar.addMenu('快速打开窗口')
		self.optimize_menu_item.addAction('Namespace Editor', self.NamespaceEditor_win)
		self.optimize_menu_item.addAction('Node Editor', self.NodeEditor_win)
		self.optimize_menu_item.addAction('Graph Editor', self.GraphEditor_win)
		self.optimize_menu_item.addAction('Shape Editor', self.ShapeEditor_win)
		
		self.pluging_menu_item = self.menu_bar.addMenu('插件')
		self.pluging_menu_item.addAction('DNA查看器 Dna_Viewer v2.1.1', self.dna_viewer_win)
		self.pluging_menu_item.addAction('权重编辑v2.3.0', self.weights_editor_win)       
		self.pluging_menu_item.addAction('权重导入导出 v1.3.0', self.skinner_win)  
		self.pluging_menu_item.addAction('Rig_Adjustment v2.0.0', self.rig_adjustment_win)
		self.pluging_menu_item.addAction('姿态管理器 epic_pose_wrangler v2.0.0', self.epic_pose_wrangler_win)


		
		self.about_menu_item = self.menu_bar.addMenu('关于')
		self.about_menu_item.addAction('开发感言', self.Development_Reflection_log_win)




		self.disconnect_joint_connections = QtWidgets.QPushButton()
		self.disconnect_joint_connections.setIcon(QtGui.QIcon(icon_path+'disconnect.png'))
		self.disconnect_joint_connections.setIconSize(QtCore.QSize(35, 35))
		self.disconnect_joint_connections.setFixedSize(50, 50)
		self.disconnect_joint_connections.clicked.connect(self.disconnect_joint_connections_win)

		self.connect_joint_nodes = QtWidgets.QPushButton()
		self.connect_joint_nodes.setIcon(QtGui.QIcon(icon_path+'connect.png'))
		self.connect_joint_nodes.setIconSize(QtCore.QSize(35, 35))
		self.connect_joint_nodes.setFixedSize(50, 50)
		self.connect_joint_nodes.clicked.connect(self.connect_joint_nodes_win)		
  
		self.load_path_note = QtWidgets.QLabel(' DNA加载路径:')
		self.load_dna_path = QtWidgets.QLineEdit(DSM.reading_history_file()['load_dna_path'])
		self.load_dna_path.textChanged.connect(self.save_path_data)
		#...路径加载按钮
		self.manual_load_file_selection = QtWidgets.QPushButton('...')
		self.manual_load_file_selection.clicked.connect(self.manual_file_selection_win)
		self.manual_load_file_selection.setFixedSize(50, 35)
		
		self.load_dna_path_open = QtWidgets.QPushButton('Open')
		self.load_dna_path_open.clicked.connect(self.load_dna_path_open_win)
		self.load_dna_path_open.setFixedSize(80, 35) 

		
		self.create_mesh = QtWidgets.QPushButton("构建头部")
		self.create_mesh.clicked.connect(self.create_mesh_win)
		
		self.save_new_modify_dna = QtWidgets.QPushButton("修改后保存DNA")
		self.save_new_modify_dna .clicked.connect(self.save_new_modify_dna_win)
		
		self.build_rig_maya_scene = QtWidgets.QPushButton("组装到场景")
		self.build_rig_maya_scene .clicked.connect(self.build_rig_maya_scene_win)        
		

		self.create_body_mesh = QtWidgets.QPushButton("构建身体")
		self.create_body_mesh .clicked.connect(self.create_body_mesh_win)
		
		self.fix_body_joint = QtWidgets.QPushButton("对齐固定身体")
		self.fix_body_joint.clicked.connect(self.fix_body_joint_win) 
	 
		self.quicke_rename = QtWidgets.QPushButton('快速命名')
		self.quicke_rename.clicked.connect(self.quicke_rename_win)

		self.rig_adjustment = QtWidgets.QPushButton('匹配')
		self.rig_adjustment.clicked.connect(self.rig_adjustment_win)
		self.rig_adjustment.setFixedSize(50, 38)    

		self.X_ray = QtWidgets.QPushButton("xRay")
		self.X_ray.clicked.connect(self.X_ray_win)
		self.X_ray.setFixedSize(50, 38) 

		self.animation_data_import_tool = QtWidgets.QPushButton('动画数据导入')
		self.animation_data_import_tool.clicked.connect(self.animation_data_import_tool_win)
		
		self.BlendShapeInput_Modifier_Window = QtWidgets.QPushButton("输入BS修改器")
		self.BlendShapeInput_Modifier_Window.clicked.connect(self.BlendShapeInput_Modifier_Window_win)       
		
		self.Joint_transformation_Window = QtWidgets.QPushButton("关节变换编辑器")
		self.Joint_transformation_Window.clicked.connect(self.Joint_Transformation_Editor_win)    

		self.Blend_Shape_Editor_Window = QtWidgets.QPushButton("BS编辑器")
		self.Blend_Shape_Editor_Window.clicked.connect(self.Blend_Shape_Editor_win)
  
		self.test = QtWidgets.QPushButton("test")
		self.test.clicked.connect(self.test_win)

		

		#...分割线
		self.separator = QtWidgets.QFrame()
		self.separator.setFrameShape(QtWidgets.QFrame.HLine)
		self.separator.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.separator1 = QtWidgets.QFrame()
		self.separator1.setFrameShape(QtWidgets.QFrame.HLine)
		self.separator1.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.separator2 = QtWidgets.QFrame()
		self.separator2.setFrameShape(QtWidgets.QFrame.HLine)
		self.separator2.setFrameShadow(QtWidgets.QFrame.Sunken)
	def create_layouts(self):
		
		load_dna_path_layout_00 = QtWidgets.QHBoxLayout()
		load_dna_path_layout_00.addWidget(self.disconnect_joint_connections)
		load_dna_path_layout_00.addWidget(self.connect_joint_nodes)
		# 往左对齐设置
		load_dna_path_layout_00.setAlignment(QtCore.Qt.AlignLeft)
  
  
		load_dna_path_layout = QtWidgets.QHBoxLayout()
		load_dna_path_layout.addWidget(self.load_path_note)
		load_dna_path_layout.addWidget(self.load_dna_path)
		load_dna_path_layout.addWidget(self.manual_load_file_selection)
		load_dna_path_layout.addWidget(self.load_dna_path_open)
		
		


		create_builder_layout_01 = QtWidgets.QHBoxLayout()
		create_builder_layout_01.addWidget(self.X_ray)
		create_builder_layout_01.addWidget(self.rig_adjustment) 
		create_builder_layout_01.addWidget(self.create_mesh)
		create_builder_layout_01.addWidget(self.save_new_modify_dna)
		create_builder_layout_01.addWidget(self.build_rig_maya_scene)
		create_builder_layout_01.addWidget(self.create_body_mesh)     
		create_builder_layout_01.addWidget(self.fix_body_joint)  

		
		create_builder_layout_02 = QtWidgets.QHBoxLayout()
		create_builder_layout_02.addWidget(self.quicke_rename)  
		create_builder_layout_02.addWidget(self.animation_data_import_tool)
		create_builder_layout_02.addWidget(self.BlendShapeInput_Modifier_Window)
		create_builder_layout_02.addWidget(self.Joint_transformation_Window)
		create_builder_layout_02.addWidget(self.Blend_Shape_Editor_Window)

		
		create_builder_layout_02.addWidget(self.test)

		main_layout = QtWidgets.QVBoxLayout(self)
		
		#...菜单layout
		main_layout.addWidget(self.menu_bar)
		main_layout.addLayout(load_dna_path_layout_00)
		main_layout.addLayout(load_dna_path_layout)
		main_layout.addLayout(create_builder_layout_01)
		main_layout.addWidget(self.separator)
		main_layout.addLayout(create_builder_layout_02)


	def rig_adjustment_win(self):
		#https://github.com/revoconner/Universal-Rig-Adapter
		import rev_rig_adjustment
		rev_rig_adjustment.RevUI()     
		
	def skinner_win(self):
		# https://github.com/AKEric/skinner#export-features
		from skinner import skinner_window
		skinner_window.App()
		
	def dna_viewer_win(self):
		import dna_viewer
		dna_viewer.show()
		
	def metahuman_facial_win(self):
		#https://github.com/swnolan/metahuman_facial_transfer
		import metahuman_facial_transfer 
		importlib.reload(metahuman_facial_transfer)
		metahuman_facial_transfer.UI()
		
	def weights_editor_win(self):
		#https://github.com/theRussetPotato/weights_editor
		import weights_editor_tool.weights_editor
		weights_editor_tool.weights_editor.run()        

	def epic_pose_wrangler_win(self):
		#https://github.com/carli0215/poseWrangler_metahuman
		
		from epic_pose_wrangler import main
		main.PoseWrangler()

	def manual_file_selection_win(self):
		path = QtWidgets.QFileDialog.getOpenFileName(self, '选择文件')

		path = path[0].replace("\\", "/")
		
		self.load_dna_path.setText(path)
		
		return path
	
	def load_dna_win(self):
		global reader
		path = self.load_dna_path.text()
		
		reader = DNA_ET.load_dna(path)
		
		return reader
	
	def save_new_modify_dna_win(self):
		path = self.load_dna_path.text()
		save_path = self.save_path_auto_create()
		DNA_ET.save_new_modify(path,save_path)
		
	def create_mesh_win(self):
		DNA_ET.building_the_meshes(self.load_dna_path.text())
		
	def build_rig_maya_scene_win(self):
		DNA_ET.assemble_maya_scene(self.load_dna_path.text())
		
	def create_body_mesh_win(self):
		DNA_ET.building_body_the_meshes()
	
	def fix_body_joint_win(self):
		DNA_ET.fix_body()
		DNA_ET.connect_body()
	
	def optimize_dna_scene_win(self):
		DNA_ET.optimize_scene()
	
	def save_path_auto_create(self):
		load_dna_path = self.load_dna_path.text()
		#...获取路径前缀后后缀
		if load_dna_path == '':
			print('注意：请你输入加载路径才可以自动生成保存路径')
			return
		path_dirname = os.path.dirname(load_dna_path)
		path_basename = os.path.basename(load_dna_path)
		path_basename = path_basename.replace('.dna','')
		path_basename = path_basename + "_NewModifyLast.dna"
		save_path = path_dirname+"\\"+path_basename
		return save_path.replace("\\", "/")
	

	def dna_clear_blend_shapes_win(self): #...删除bs
		path = self.load_dna_path.text()
		save_path = self.save_path_auto_create()
		DNA_ET.clear_blend_shapes(path,save_path)

	def dna_data_dict_win(self):
		dna_data_dict = DNA_ET.get_dna_all_data(self.load_dna_path.text())
		print('<<<<<' * 10)
		for key_name in dna_data_dict:
			key_data = dna_data_dict[key_name]
			print(f'DNA的{key_name}：{key_data}')
		print('>>>>>' * 10)


	def NamespaceEditor_win(self):
		mel.eval("NamespaceEditor")
  
	def NodeEditor_win(self):
		cmds.NodeEditorWindow()
  
	def GraphEditor_win(self):
		mel.eval("GraphEditor")
  
	def ShapeEditor_win(self):
		mel.eval("ShapeEditor")
		
	def dna_binary_to_json_win(self):
		DNA_ET.binary_to_json(self.load_dna_path.text(),self.save_path_auto_create())

	def BlendShapeInput_Modifier_Window_win(self):
		BlendShapeInput_Modifier_Window = DNA_ET.BlendShapeInput_Modifier_Window()
		BlendShapeInput_Modifier_Window.show()

	def quicke_rename_win(self):
		DNA_ET.quicke_rename_mesh()  
		
	def X_ray_win(self):
		DNA_ET.xRay_display()

	def descriptor_modify_win(self):
		descriptor_modify_win = DNA_ET.Descriptor_Modify_Window(self.load_dna_path.text(),self.save_path_auto_create())
		descriptor_modify_win.show()

	def load_dna_path_open_win(self):
		path = os.path.dirname(self.load_dna_path.text())
		os.startfile(path)



	def calculate_lower_lod_mesh_win(self):
		DNA_ET.CalculateMeshLowerLODs(self.load_dna_path.text(),self.save_path_auto_create())

	def test_win(self):
		# Set_Joint_Translation_Tool_Window = DNA_ET.Set_Joint_Tool_Window()
		# Set_Joint_Translation_Tool_Window.show()
		# MetaDnaEdit  = DNA_ET.MetaDnaEdit()
		# MetaDnaEdit.show()
		MetaDnaEdit  = DNA_ET.test(self.load_dna_path.text())
	def animation_data_import_tool_win(self):
		animation_data_import_tool_win = DNA_ET.Animation_Data_Import_Tool_Window()
		animation_data_import_tool_win.show()   

	def save_path_data(self):
		load_dna_path = self.load_dna_path.text()
		DSM.modify_file_attr('load_dna_path',load_dna_path)

	def Development_Reflection_log_win(self):
		Development_Reflection_log_win = Development_Reflection_log()
		Development_Reflection_log_win.show()

	def body_processing_win(self):
		DNA_ET.body_processing()

	def disconnect_joint_connections_win(self):
		DNA_ET.disconnect_joint_connections()
  
	def connect_joint_nodes_win(self):
		DNA_ET.connect_joint_nodes()
  
	def Joint_Transformation_Editor_win(self):
		Set_Joint_Tool_Window = DNA_ET.Set_Joint_Tool_Window()
		Set_Joint_Tool_Window.show()
  
	def Blend_Shape_Editor_win(self):
		save_path = self.save_path_auto_create()
		Blend_Shape_Editor_Window = DNA_ET.Blend_Shape_Editor_Window(save_path)
		Blend_Shape_Editor_Window.show()
def delete_module(module_name): #...检测是否有库，如果有就卸载库
	# 检查模块是否已经被导入
	if module_name in sys.modules:
		# 如果已经被导入，那么删除它
		del sys.modules[module_name]       
		print(f"模块 {module_name} 已经被删除")

	else:
		print(f"模块 {module_name} 没有被导入")



info = '''现在是这个MPP多功能Metahuman的v0.5的版本。
开发一共使用了10天左右的时间。
第一周我对dna的三个库真的一点都不理解，
很庆幸我可以坚持下来并且开发出这个脚本。
在这个过程我真的经历了很多一些压力很大的状况包括现状，
很困难，很孤独，但开发完成还是很开心，
第二周舒服很多了，对这些库了解的比较熟悉了。
但颈椎旁边的肌肉真的很僵硬！！！！

感谢一路支持我的小伙伴。
给我带来动力！
我希望可以获得多一点的陪伴和关心！


  
  
  
  
  
					Salute 
	
					---Amazing_iKe
					2023/11/26
'''

class Development_Reflection_log(QtWidgets.QDialog):
	
	WIN_NAME = "DRL_WIN"
	TITLE = '我的个人开发感想 --Amazing_iKe'
	
	def __init__(self, parent=maya_main_window()):

		super(Development_Reflection_log, self).__init__(parent)


		if cmds.window(Development_Reflection_log.WIN_NAME, exists=True):
			cmds.deleteUI(Development_Reflection_log.WIN_NAME)
				
		#...窗口名字
		self.setObjectName(Development_Reflection_log.WIN_NAME)
		self.setWindowTitle(Development_Reflection_log.TITLE)


				
		bold_font = QtGui.QFont()
		bold_font.setBold(True)
		bold_font.setPixelSize(20)
		bold_font.setFamily("Microsoft YaHei") 
		
		layout = QtWidgets.QVBoxLayout()
		self.setLayout(layout)
		
		scroll_area = QtWidgets.QScrollArea()
		scroll_area.setWidgetResizable(True)
		layout.addWidget(scroll_area)
		
		container = QtWidgets.QWidget()
		container_layout = QtWidgets.QVBoxLayout()
		container.setLayout(container_layout)
		scroll_area.setWidget(container)
		
		text_edit = QtWidgets.QPlainTextEdit(info)
		text_edit.setReadOnly(True)
		text_edit.setFont(bold_font)
		container_layout.addWidget(text_edit)
		
		button = QtWidgets.QPushButton("Close")
		button.clicked.connect(self.close)
		container_layout.addWidget(button)
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.setMinimumSize(675, 800)

def Main_program():
	DSM.Detect_and_create_history_folder()
	DSM.Detect_and_create_history_file()
	d = MMP_MAIN_UI()
	d.show()

