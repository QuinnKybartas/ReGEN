from Tkinter import *
from Readers import *
from Writers import *
from SocialGraph import *
import tkFileDialog

class GraphBuilder:
	
	def __init__(self, master):
		self.master = master
		self.frame = Frame(master, width=1280, height=760)

		self.loaded = False
		self.cur_node_sel = -1
		
		listboxwidth = 30
		
		self.buttons = {}
		self.labels = {}
		self.stringvar = {}
		self.entries = {}
		self.listboxes = {}
		self.scrollbars = {}
		
		self.nodes = {}
		self.edges = {}
		
		self.mainframe = Frame(self.frame)
		self.upperbuttonframe = Frame(self.frame)
		self.lowerbuttonframe = Frame(self.frame)
		
		self.graphname = Frame(self.mainframe)
		self.nodesframe = Frame(self.mainframe)
		
		self.connections = Frame(self.nodesframe, relief=SUNKEN, borderwidth=1)
		self.nodeslist = Frame(self.nodesframe, relief=SUNKEN, borderwidth=1)
		self.nodedetails = Frame(self.nodesframe, relief=SUNKEN, borderwidth=1)
		
		#------------------------------------------------------------------------------------------------
		
		self.labels["GraphName"] = Label(self.graphname, text="Graph Name:")
		self.labels["GraphName"].grid(row=0, column=0)
		
		self.labels["NodeList"] = Label(self.nodeslist, text="Node List:")
		self.labels["NodeList"].grid(row=0, column=0)
		
		self.labels["NodeDetails"] = Label(self.nodedetails, text="Node Details")
		self.labels["NodeDetails"].grid(row=0, column=0, columnspan=2)
		
		self.labels["NodeName"] = Label(self.nodedetails, text="Name:")
		self.labels["NodeName"].grid(row=1, column=0)
		
		self.labels["NodeAttributes"] = Label(self.nodedetails, text="Attributes:")
		self.labels["NodeAttributes"].grid(row=3, column=0)
		
		self.labels["Connections"] = Label(self.connections, text="Connections:")
		self.labels["Connections"].grid(row=0,column=0)
		#-------------------------------------------------------------------------------------------------
		
		self.stringvar["GraphName"] = StringVar()
		self.entries["GraphName"] = Entry(self.graphname, width=70, textvariable=self.stringvar["GraphName"])
		self.entries["GraphName"].grid(row=1,column=1)
		
		self.stringvar["NodeName"] = StringVar()
		self.entries["NodeName"] = Entry(self.nodedetails, width=listboxwidth, state='readonly', textvariable = self.stringvar["NodeName"])
		self.entries["NodeName"].grid(row=2,column=1,columnspan=2)
		
		#-------------------------------------------------------------------------------------------------
		
		self.scrollbars["NodeList"] = Scrollbar(self.nodeslist, orient=VERTICAL)
		self.listboxes["NodeList"] = Listbox(self.nodeslist, width=listboxwidth, height=30, yscrollcommand=self.scrollbars["NodeList"].set)
		self.scrollbars["NodeList"].config(command=self.listboxes["NodeList"].yview)
		self.scrollbars["NodeList"].grid(row=1, column=1, sticky=N+S)
		self.listboxes["NodeList"].grid(row=1, column=2)

		self.scrollbars["NodeAttributes"] = Scrollbar(self.nodedetails, orient=VERTICAL)	
		self.listboxes["NodeAttributes"] = Listbox(self.nodedetails, width=listboxwidth, height=26, yscrollcommand=self.scrollbars["NodeAttributes"].set)
		self.scrollbars["NodeAttributes"].config(command=self.listboxes["NodeAttributes"].yview)
		self.scrollbars["NodeAttributes"].grid(row=4, column=1, sticky=N+S)
		self.listboxes["NodeAttributes"].grid(row=4, column=2, sticky=W)

		self.scrollbars["Connections"] = Scrollbar(self.connections, orient=VERTICAL)	
		self.listboxes["Connections"] = Listbox(self.connections, width=listboxwidth * 2, height=30, yscrollcommand=self.scrollbars["Connections"].set)
		self.scrollbars["Connections"].config(command=self.listboxes["Connections"].yview)
		self.scrollbars["Connections"].grid(row=1, column=1, sticky=N+S)
		self.listboxes["Connections"].grid(row=1, column=2, sticky=W)		
		#-------------------------------------------------------------------------------------------------
				
		self.buttons["New"] =  Button(self.upperbuttonframe, text="New Node", command=self.newNode)
		self.buttons["New"].pack(side=LEFT)
		
		self.buttons["Edit"] =  Button(self.upperbuttonframe, text="Edit Node", command=self.editNode)
		self.buttons["Edit"].pack(side=LEFT)
		
		self.buttons["Delete"] =  Button(self.upperbuttonframe, text="Delete Node", command=self.deleteNode)
		self.buttons["Delete"].pack(side=LEFT)
		
		self.buttons["NewCon"] =  Button(self.upperbuttonframe, text="New Connection", command=self.newConnection)
		self.buttons["NewCon"].pack(side=LEFT)
		
		self.buttons["EditCon"] =  Button(self.upperbuttonframe, text="Edit Connection", command=self.editConnection)
		self.buttons["EditCon"].pack(side=LEFT)
		
		self.buttons["DeleteCon"] =  Button(self.upperbuttonframe, text="Delete Connection", command=self.deleteConnection)
		self.buttons["DeleteCon"].pack(side=LEFT)
		
		self.buttons["Load"] = Button(self.lowerbuttonframe, text="Load", command=self.loadGraph)
		self.buttons["Load"].pack(side=LEFT)
		
		self.buttons["Save"] = Button(self.lowerbuttonframe, text="Save", command=self.saveGraph)
		self.buttons["Save"].pack(side=LEFT)
		
		self.buttons["SaveQuit"] = Button(self.lowerbuttonframe, text="Save and Quit", command=self.saveandQuit)
		self.buttons["SaveQuit"].pack(side=LEFT)
		
		self.buttons["Quit"] = Button(self.lowerbuttonframe, text="Quit", command=self.frame.quit)
		self.buttons["Quit"].pack(side=LEFT)
		
		#-------------------------------------------------------------------------------------------------
				
		self.nodeslist.grid(row=0, column=0, sticky=N)
		self.nodedetails.grid(row=0, column=1,sticky=N, padx=25)
		self.connections.grid(row=0, column=2,sticky=N)
		self.graphname.grid(row=0, pady=25, padx=5)
		self.nodesframe.grid(row=1, sticky=W, padx=5, pady=5)
		self.mainframe.grid(row=0)
		self.upperbuttonframe.grid(row=1, sticky=S)
		self.lowerbuttonframe.grid(row=2, sticky=S)

		#self.hi_there.bind("<Enter>", self.changecolor)

		self.frame.pack()
		menu = Menu(self.frame)
		master.config(menu=menu)
		
		filemenu = Menu(menu)
		menu.add_cascade(label="File", menu=filemenu)
		filemenu.add_command(label="New", command=self.newGraph)
		filemenu.add_command(label="Load", command=self.loadGraph)
		filemenu.add_command(label="Save", command=self.saveGraph)
		filemenu.add_separator()
		filemenu.add_command(label="Save and Exit", command=self.saveandQuit)
		filemenu.add_command(label="Exit", command=self.frame.quit)
		addmenu = Menu(menu)
		menu.add_cascade(label="Add", menu=addmenu)
		addmenu.add_command(label="Node", command=self.newNode)
		addmenu.add_command(label="Connection", command=self.newConnection)
		editmenu = Menu(menu)
		menu.add_cascade(label="Edit", menu=editmenu)
		editmenu.add_command(label="Node", command=self.editNode)
		editmenu.add_command(label="Connection", command=self.editConnection)
		deletemenu = Menu(menu)
		menu.add_cascade(label="Delete", menu=deletemenu)
		deletemenu.add_command(label="Node", command=self.deleteNode)
		deletemenu.add_command(label="Connection", command=self.deleteConnection)
	
		self.poll()
		
	def newGraph(self):
		print "New Graph"
		
	def saveandQuit(self):
		self.saveGraph()
		self.master.destroy()
		
	def loadGraph(self):
		filename = tkFileDialog.askopenfilename(title='LoadWorldGraph', filetypes=[('TXT', ('*.txt'))])
		if filename:
			self.cleanAll()
			GraphReader = SocialGraphReader(filename)
			self.graph = GraphReader.readGraph()
			self.stringvar["GraphName"]
			self.stringvar["GraphName"].set(self.graph.get_name())
		
			for node in self.graph.get_nodes():
				self.listboxes["NodeList"].insert(END, node.get_name())
				self.nodes[node.get_name()] = node
			
			if len(self.graph.get_nodes()) > 0:
				self.listboxes["NodeList"].selection_set(0)
			
			for edge in self.graph.get_edges():
				name = edge.get_from_node().get_name() + " { " + edge.get_key() + " : " + edge.get_value() + " } " + edge.get_to_node().get_name() 
				self.listboxes["Connections"].insert(END, name)
				self.edges[name] = edge
				
			self.loaded = True
			
	def poll(self):
		if len(self.listboxes["NodeList"].curselection()) == 1:
			num = self.listboxes["NodeList"].curselection()[0]
			if not num == self.cur_node_sel:
				self.cur_node_sel = num
				name = self.listboxes["NodeList"].get(num)
				node = self.nodes[name]
				self.stringvar["NodeName"].set(name)

				self.listboxes["NodeAttributes"].delete(0, END)				
				for attr in node.get_attributes():
					name = attr + " : " + str(node.get_attributes()[attr])
					self.listboxes["NodeAttributes"].insert(END, name)
		self.frame.after(50, self.poll)

	def cleanAll(self):
		self.loaded = False
		self.cur_node_sel = -1
		for var in self.stringvar:
			self.stringvar[var].set("")
		for box in self.listboxes:
			self.listboxes[box].delete(0, END)

	def saveGraph(self):
		filename = tkFileDialog.asksaveasfilename(title='SaveWorldGraph', filetypes=[('TXT', ('*.txt'))], initialfile=self.stringvar['GraphName'].get())
		
		if filename:
			writer = SocialGraphWriter(self.graph)
			writer.writeGraph(filename)
			
	def newNode(self):
		print "New Node"
	
	def editNode(self):
		print "Edit Node"
	
	def deleteNode(self):
		print "Delete Node"
		
	def newConnection(self):
		print "New Connection"
	
	def editConnection(self):
		print "Edit Connection"
	
	def deleteConnection(self):
		print "Delete Connection"

	def clear(self):
		print "Clear"
		
	def changecolor(self, event):
		print "WOPA"
		
	def say_hi(self):
		print "Hi There!"
		
	def newConnection(self):
		print "New Connections"

root = Tk()
root.wm_title("Social Graph Editor")

build = GraphBuilder(root)

root.mainloop()
