import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, \
    QGridLayout,QMessageBox,QProgressBar,QCheckBox,QStatusBar,QLineEdit,QFileDialog,QLabel,QTableWidgetItem,QInputDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import atexit
import pickle
import subprocess, signal, os
import msg_parser
import multiprocessing as mp
import setproctitle as spt
import time
import agent
import igraph
from PyQt5.QtSvg import QSvgWidget, QGraphicsSvgItem
import sys
from PyQt5 import QtCore

graph_path = ""
graph_path2 = ""
global_agents = 50
global_edges = 5
agents_procs = []

class App(QDialog):

    def __init__(self):
        super().__init__()
        self.title = 'Pronios Thesis Launcher'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 100
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createGridLayout()

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        windowLayout.addWidget(self.horizontalGroupBox3)

        windowLayout.addWidget(self.horizontalGroupBox4)
        windowLayout.addWidget(self.horizontalGroupBox2)

        self.setLayout(windowLayout)
        self.agents_no.setText(str(global_agents))
        self.graph_nodes_ln.setText(str(global_agents))
        self.graph_edges_ln.setText(str(global_edges))

        self.new_graph.toggle()
        self.show()

    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox("Simulation Settings")
        layout = QGridLayout()
        #layout.setColumnStretch(1, 4)
        #layout.setColumnStretch(2, 4)

        file_button_1 = QPushButton("Select File")
        file_button_1.clicked.connect(self.open_file_method)

        file_button_2 = QPushButton("Select File")
        file_button_2.clicked.connect(self.open_file_method2)

        agent_button = QPushButton("Agents #")
        agent_button.clicked.connect(self.getInteger)

        start_button = QPushButton("Start")
        start_button.clicked.connect(self.start_sim)

        stop_button = QPushButton("Stop")
        stop_button.clicked.connect(self.stop_sim)

        self.create_graph_b = QPushButton("Create New Graph")
        self.create_graph_b.clicked.connect(self.create_graph)

        self.show_3d_b = QPushButton("3D")
        self.show_3d_b.clicked.connect(self.show_3d_m)

        self.graph_loc = QLineEdit(self)
        self.graph_loc2 = QLineEdit(self)
        self.agents_no = QLineEdit(self)

        self.graph_nodes_ln = QLineEdit(self)
        self.graph_edges_ln = QLineEdit(self)

        layout.addWidget(QLabel('Graph File'), 0, 0)

        layout.addWidget(self.graph_loc, 1, 0)
        layout.addWidget(file_button_1, 1, 1)

        layout.addWidget(QLabel('Settings File'), 2, 0)

        layout.addWidget(self.graph_loc2, 3, 0)
        layout.addWidget(file_button_2, 3, 1)

        layout.addWidget(QLabel('Number Of Agents'), 4, 0)

        layout.addWidget(agent_button, 5, 1)
        layout.addWidget(self.agents_no, 5, 0)

        self.new_graph = QCheckBox("Use Existing Graph", self)
        self.new_graph.stateChanged.connect(self.new_graph_opt)

        self.horizontalGroupBox.setLayout(layout)

        self.horizontalGroupBox2 = QGroupBox("Progress")
        layout2 = QGridLayout()
        #layout2.setColumnStretch(1, 4)
        #layout2.setColumnStretch(2, 4)


        self.progress = QProgressBar(self)
        #self.progress
        layout2.addWidget(self.progress, 0, 0)

        self.horizontalGroupBox2.setLayout(layout2)

        self.horizontalGroupBox3 = QGroupBox("Sim")
        layout3 = QGridLayout()
        layout3.addWidget(start_button, 0, 0)
        layout3.addWidget(stop_button, 0, 1)
        self.horizontalGroupBox3.setLayout(layout3)
        self.graph_loc.setText(graph_path)
        self.graph_loc2.setText(graph_path2)

        self.horizontalGroupBox4 = QGroupBox("Graph Options")
        layout4 = QGridLayout()
        layout4.addWidget(self.create_graph_b, 0, 1)
        layout4.addWidget(QLabel('Number Of Nodes'), 1, 0)
        layout4.addWidget(self.graph_nodes_ln, 2, 0)
        layout4.addWidget(QLabel('Number Of Edges'), 1, 1)
        layout4.addWidget(self.graph_edges_ln, 2, 1)
        layout4.addWidget(self.new_graph, 0, 0)
        layout4.addWidget(self.show_3d_b, 3, 0)

        self.horizontalGroupBox4.setLayout(layout4)

    def open_file_method(self):
        self.fd = file_dialog_graph(self)
        self.fd.show()
        self.graph_loc.setText(graph_path)
        #self.show()

    def open_file_method2(self):
        self.fd = file_dialog_graph2(self)
        self.fd.show()
        self.graph_loc2.setText(graph_path2)

    def getInteger(self,value):
        global global_agents
        global_agents, okPressed = QInputDialog.getInt(self, "Get integer", "Number:", 50, 0, 200, 1)
        if okPressed:
            print(global_agents)
        self.agents_no.setText(str(global_agents))
        self.graph_nodes_ln.setText(str(global_agents))

    def show_3d_m(self):
        self.s3d = show_3d(self)

    def start_sim(self):
        #self.progress.setValue(50)

        global agents_procs
        for i in range(global_agents):

            p = mp.Process(target=agent.main(i,graph_path))#,str(5000 + 2 * i),str(5000 + 2 * i + 1)))
            p.daemon = True
            agents_procs.append(p)
            p.start()
            prog = (i+1)/global_agents*100
            #print(prog)
            self.progress.setValue(prog)

        if False:
            for a in range(global_agents):
                os.system("agent.py "+str(a))

        if False:
            for a in range(global_agents):
                os.system("agent.py "+str(a))
                #import the agent as a module, run main with args

    def stop_sim(self):
        spt.setproctitle("pronpy_closer")
        time.sleep(0.5)

        p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
        out, err = p.communicate()

        #for line in out.splitlines():
         #   if b'pronpy' in line:
          #      pid = int(line.split(None, 1)[0])
           #     os.kill(pid, signal.SIGKILL)

        i = global_agents
        for proc in agents_procs:
            i -= 1
            proc.terminate()
            print('TERMINATED:', proc, proc.is_alive())
            proc.join()
            print('JOINED:', proc, proc.is_alive())
            self.progress.setValue(100*i/global_agents)
        #os.killpg()

    def closeEvent(self, event):
        """Generate 'question' dialog on clicking 'X' button in title bar.

        Reimplement the closeEvent() event handler to include a 'Question'
        dialog with options on how to proceed - Save, Close, Cancel buttons
        """
        reply = QMessageBox.question(
            self, "Message",
            "Are you sure you want to quit? Any unsaved work will be lost.",
            QMessageBox.Save | QMessageBox.Close | QMessageBox.Cancel,
            QMessageBox.Save)

        if reply == QMessageBox.Close:
            event.accept()
            self.stop_sim()
        elif reply == QMessageBox.Save:
            save_meta()
            self.stop_sim()
            event.accept()
        else:
            event.ignore()

    def new_graph_opt(self, state):

        if state == QtCore.Qt.Checked:
            self.create_graph_b.setEnabled(False)
            self.graph_edges_ln.setEnabled(False)
            self.graph_nodes_ln.setEnabled(False)
        else:
            self.create_graph_b.setEnabled(True)
            self.graph_edges_ln.setEnabled(True)
            self.graph_nodes_ln.setEnabled(True)

    def create_graph(self):
        nodes = global_agents
        degree = int(self.graph_edges_ln.text())
        g = igraph.Graph.K_Regular(nodes, degree, directed=True, multiple=False)
        g = g.as_undirected()
        st = g.spanning_tree()
        st.to_directed(mutual=True)

        print(st.get_edgelist())
        for a, b in st.get_edgelist():
            #print(a, ": ", b)
            c = st.get_shortest_paths(0, to=a)
            d = st.get_shortest_paths(0, to=b)
            #print(len(c[0]), " VS: ", len(d[0]))

            if len(c[0]) > len(d[0]):
                st.add_edge(b, a)
                st.delete_edges([st.get_eid(a, b, directed=True)])
            # print (st)
            else:
                st.add_edge(a, b)
                st.delete_edges([st.get_eid(a, b, directed=True)])

        st.write_svg("st2.svg", layout='auto', width=600, height=400,
                     labels='label', colors='color', shapes='shape', vertex_size=10,
                     edge_colors='color', font_size=16)

        st.write_pickle("st_pickle", version=-1)

        self.ssvg = show_svg(self)


class file_dialog_graph(QWidget):

    def __init__(self, parent):
        super(file_dialog_graph, self).__init__(parent)
        self.title = 'Chose the graph File..'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI(parent)

    def initUI(self,parent):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.openFileNameDialog(parent)

    def openFileNameDialog(self,parent):
        global graph_path
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            graph_path=fileName
            print(fileName)
        super(file_dialog_graph, self).__init__(parent)

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "",
                                                "All Files (*);;Python Files (*.py)", options=options)
        if files:
            print(files)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)


class file_dialog_graph2(QWidget):

    def __init__(self, parent):
        super(file_dialog_graph2, self).__init__(parent)
        self.title = 'Chose the graph File..'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI(parent)

    def initUI(self,parent):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.openFileNameDialog(parent)
        #self.openFileNamesDialog()
        #self.saveFileDialog()

        #self.show()


    def openFileNameDialog(self,parent):
        global graph_path2
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            graph_path2=fileName
            print(fileName)
        super(file_dialog_graph2, self).__init__(parent)

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "",
                                                "All Files (*);;Python Files (*.py)", options=options)
        if files:
            print(files)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)


class show_svg(QWidget):

    def __init__(self, parent):
        super(show_svg, self).__init__(parent)
        self.title = 'Created a Spanning Tree'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI(parent)

    def initUI(self,parent):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        #self.openFileNamesDialog()
        #self.saveFileDialog()
        #label = QLabel(self)
        self.svg = QSvgWidget('st2.svg')
        #self.svg.s
        #self.show()

        self.svg.show()

class show_3d(QWidget):

    def __init__(self, parent):
        super(show_svg, self).__init__(parent)
        self.title = 'Created a Spanning Tree'
        self.left = 10
        self.top = 10
        self.width = 800
        self.height = 800
        self.initUI(parent)

    def initUI(self,parent):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        st = igraph.Graph.Read_Pickle(graph_path)

        layt = st.layout('kk', dim=3)

        Edges=  (igraph.Graph.get_edgelist(st))
        N = global_agents
        Xn = [layt[k][0] for k in range(N)]  # x-coordinates of nodes
        Yn = [layt[k][1] for k in range(N)]  # y-coordinates
        Zn = [layt[k][2] for k in range(N)]  # z-coordinates
        Xe = []
        Ye = []
        Ze = []
        for e in Edges:
            Xe += [layt[e[0]][0], layt[e[1]][0], None]  # x-coordinates of edge ends
            Ye += [layt[e[0]][1], layt[e[1]][1], None]
            Ze += [layt[e[0]][2], layt[e[1]][2], None]

        trace1 = Scatter3d(x=Xe,
                           y=Ye,
                           z=Ze,
                           mode='lines',
                           line=Line(color='rgb(125,125,125)', width=1),
                           hoverinfo='none'
                           )
        trace2 = Scatter3d(x=Xn,
                           y=Yn,
                           z=Zn,
                           mode='markers',
                           name='actors',
                           marker=Marker(symbol='dot',
                                         size=6,
                                         color=group,
                                         colorscale='Viridis',
                                         line=Line(color='rgb(50,50,50)', width=0.5)
                                         ),
                           text=labels,
                           hoverinfo='text'
                           )

        self.svg.show()


def save_meta():
    file_Name = "dat"
    fo = open(file_Name, 'wb')
    prev = [graph_path, graph_path2]
    pickle.dump(prev, fo)
    fo.close()

def open_meta():
    global graph_path,graph_path2
    flag = 1
    try:
        fo = open("dat", 'rb')
        flag = 0
    except IOError:
        flag = 1

    if flag==0 :
        prev = pickle.load(fo)
        graph_path = str(prev[0])
        graph_path2 = str(prev[1])
        fo.close()
    else:
        graph_path = ""
        graph_path2 = ""

def kill_procs():
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()

    for line in out.splitlines():
       if b'pronpy' in line:
          pid = int(line.split(None, 1)[0])
          os.kill(pid, signal.SIGKILL)



if __name__ == '__main__':
    spt.setproctitle("pronpy")
    open_meta()
    atexit.register(save_meta)
    atexit.register(kill_procs)
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())