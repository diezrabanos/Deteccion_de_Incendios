import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import math
import time

from qgis.core import *
import qgis.utils
from qgis.gui import QgsMessageBar

erroralidada=1

iface=qgis.utils.iface
#selecciono la capa de las torretas
layer = QgsVectorLayer('O:/sigmena/carto/INCENDIO/INFRAEST/42_Puestos_vigilancia_etrs89.shp', '42_Puestos_vigilancia_etrs89', 'ogr')
time.sleep(1)
#layer = iface.activeLayer()
if layer is None or (layer.type() == QgsMapLayer.RasterLayer):
    iface.messageBar().pushMessage("Warning:",  u"Seleciona la capa de los puestos de vigilancia",  QgsMessageBar.WARNING, 10) 


#genero una lista con las torres y las coordenadas
misdatos=[]
feats = [ feat for feat in layer.getFeatures() ]
for feature in feats:
    if feature.geometry().type() != QGis.Point:
        iface.messageBar().pushMessage("Warning:", u"Debe selecionar una capa de puntos", QgsMessageBar.WARNING, 10)
    point=[]

    idTM =layer.fieldNameIndex('Nombre')
    idx = layer.fieldNameIndex('x')
    idy=  layer.fieldNameIndex('y')
    point=[feature.attributes()[idTM],feature.attributes()[idx], feature.attributes()[idy]]
    misdatos.append(point)

#ordeno por el primer elemento
misdatos.sort(key=lambda x: x[0])

todaslastorretas=[""]
for point in misdatos:
    todaslastorretas.append(point[0])


class Dialog(QDialog):
    def __init__(self, parent = None):
        super(Dialog, self).__init__(parent)
        self.setWindowTitle("ALIDADAS")

        layout=QFormLayout(self)
 
        self.observador1_label=QLabel("Observador 1",self)
        self.angulo1_label=QLabel("Rumbo 1",self)
        self.angulo1_field=QLineEdit(self)
        self.linea1_label=QLabel("_______________________________",self)
        self.observador2_label=QLabel("Observador 2",self)
        self.angulo2_label=QLabel("Rumbo 2",self)
        self.angulo2_field=QLineEdit(self)
        self.linea2_label=QLabel("_______________________________",self)
        self.observador3_label=QLabel("Observador 3 (opcional)",self)
        self.angulo3_label=QLabel("Rumbo 3",self)
        self.angulo3_field=QLineEdit(self)
        self.linea3_label=QLabel("_______________________________",self)
        self.observador4_label=QLabel("Observador 4 (opcional)",self)
        self.angulo4_label=QLabel("Rumbo 4",self)
        self.angulo4_field=QLineEdit(self)
        self.linea4_label=QLabel("________________________ by SIGMENA",self)
        
        self.cb1 = QComboBox()
        self.cb2 = QComboBox()
        self.cb3 = QComboBox()
        self.cb4 = QComboBox()
        self.cb1.addItems(todaslastorretas)
        self.cb2.addItems(todaslastorretas) 
        self.cb3.addItems(todaslastorretas)
        self.cb4.addItems(todaslastorretas)          

        # OK and Cancel buttons
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel,Qt.Horizontal, self)
        
        layout.addRow(self.observador1_label)
        layout.addRow(self.cb1)
        layout.addRow(self.angulo1_label,self.angulo1_field)
        layout.addRow(self.linea1_label)
        layout.addRow(self.observador2_label)
        layout.addRow(self.cb2)      
        layout.addRow(self.angulo2_label,self.angulo2_field)
        layout.addRow(self.linea2_label)
        layout.addRow(self.observador3_label)
        layout.addRow(self.cb3)      
        layout.addRow(self.angulo3_label,self.angulo3_field)
        layout.addRow(self.linea3_label)
        layout.addRow(self.observador4_label)
        layout.addRow(self.cb4)      
        layout.addRow(self.angulo4_label,self.angulo4_field)
        layout.addRow(self.linea4_label)
        layout.addWidget(self.buttons)
        
        self.setLayout(layout)
        
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)




    # static method to create the dialog and return (date, time, accepted)
    @staticmethod
    def getParameter(parent = None):
        dialog = Dialog(parent)
        result = dialog.exec_()

        torret1=dialog.cb1.currentIndex()
        torret2=dialog.cb2.currentIndex()
        torret3=dialog.cb3.currentIndex()
        torret4=dialog.cb4.currentIndex()
        angulo1=dialog.angulo1_field.text()
        angulo2=dialog.angulo2_field.text()
        angulo3=dialog.angulo3_field.text()
        angulo4=dialog.angulo4_field.text()
        if angulo3=="":
            angulo3=9999
        if angulo4=="":
            angulo4=9999
        return (torret1,angulo1, torret2,angulo2, torret3,angulo3,torret4,angulo4,result == QDialog.Accepted)

torret1,a1,torret2,a2,torret3,a3,torret4,a4,ok = Dialog.getParameter()
#print ("{} {} {} {} {} {} {}".format(torret1,a1,torret2,a2,torret3,a3,ok))

try:
    torre1=misdatos[int(torret1)-1][0]
    x1=float(misdatos[int(torret1)-1][1])
    y1=float(misdatos[int(torret1)-1][2])
    torre2=misdatos[int(torret2)-1][0]
    x2=float(misdatos[int(torret2)-1][1])
    y2=float(misdatos[int(torret2)-1][2])
    torre3=misdatos[int(torret3)-1][0]
    x3=float(misdatos[int(torret3)-1][1])
    y3=float(misdatos[int(torret3)-1][2])
    torre4=misdatos[int(torret4)-1][0]
    x4=float(misdatos[int(torret4)-1][1])
    y4=float(misdatos[int(torret4)-1][2])
except:
    pass

try:
    ang1=float(a1)
    ang2=float(a2)
    ang3=float(a3)
    ang4=float(a4)
except:
    pass

def haceelcruce(x1,y1,ang1,x2,y2,ang2):
    #saco las pendientes
    m1=(1/math.tan(math.radians(ang1+0.000001)))
    m2=(1/math.tan(math.radians(ang2+0.000001)))
    #print m1
    #print m2

    #saco las coordenadas de x e y
    x = ((y2 - y1) + (m1*x1) - (m2*x2))/((m1 - m2)+0.000001)
    y = m1*x + y1 - m1*x1

   
    #compruebo que el cruce no es erroneo
    if a1>0 and a1<180 and x<x1 :
        iface.messageBar().pushMessage("Warning:", u"Las visuales no se cruzan", QgsMessageBar.WARNING, 10) 
    if a1>0 and a1<90 and y<y1 :
        iface.messageBar().pushMessage("Warning:", u"Las visuales no se cruzan", QgsMessageBar.WARNING, 10) 
    if a1>270 and a1<360 and y<y1 :
        iface.messageBar().pushMessage("Warning:", u"Las visuales no se cruzan", QgsMessageBar.WARNING, 10)
    if a2>0 and a2<180 and x<x2 :
        iface.messageBar().pushMessage("Warning:", u"Las visuales no se cruzan", QgsMessageBar.WARNING, 10) 
    if a2>0 and a2<90 and y<y2 :
        iface.messageBar().pushMessage("Warning:", u"Las visuales no se cruzan", QgsMessageBar.WARNING, 10) 
    if a2>270 and a2<360 and y<y2 :
        iface.messageBar().pushMessage("Warning:", u"Las visuales no se cruzan", QgsMessageBar.WARNING, 10)

    #calculo el error
    d1a=math.sqrt((x-x1)**2+(y-y1)**2)
    d2a=math.sqrt((x-x2)**2+(y-y2)**2)
    d12=math.sqrt((x2-x1)**2+(y2-y1)**2)
    A=math.acos((d1a**2+d2a**2-d12**2)/(2*d1a*d2a))
    if math.degrees(A)>90:
        A=math.pi-A
    distancias=[d1a,d2a]
    distancias.sort(reverse=True) 
    mayordistancia=distancias[0]
    
    error=mayordistancia*erroralidada/(math.sin(A/2)+0.000001)
    
    return x,y,error

#creo una capa temporal con los resultados
# create layer
vl = QgsVectorLayer("Point", "temporary_points", "memory")
pr = vl.dataProvider()
print "ok creada la capa"
def generapunto(x,y):

    vl.startEditing()
    # add fields
    pr.addAttributes([QgsField("error", QVariant.Int),
                    QgsField("x",  QVariant.Int),
                    QgsField("y", QVariant.Double)])
    vl.updateFields() 
    # tell the vector layer to fetch changes from the provider

    # add a feature
    fet = QgsFeature()
    fet.setGeometry(QgsGeometry.fromPoint(QgsPoint(x,y)))
    fet.setAttributes([error, x, y])
    pr.addFeatures([fet])

    #cambio la simbologia
    symbol = QgsMarkerSymbolV2.createSimple({'name': 'circle', 'color': 'orange','size': '5',})
    vl.rendererV2().setSymbol(symbol)

    # update layer's extent when new features have been added
    # because change of extent in provider is not propagated to the layer
    vl.updateExtents()
    vl.commitChanges()
    vl.updateExtents()
    canvas = qgis.utils.iface.mapCanvas()
    canvas.setExtent(vl.extent())


x,y,error=haceelcruce(x1,y1,ang1,x2,y2,ang2)
generapunto(x,y)

resultado=[]
resultado.append(x)
resultado.append(y)
resultado.append(error)

if ang3<>9999:
    x,y,error=haceelcruce(x1,y1,ang1,x3,y3,ang3)
    generapunto(x,y)
    if error<resultado[2]:
        resultado=[]
        resultado.append(x)
        resultado.append(y)
        resultado.append(error)
    x,y,error=haceelcruce(x2,y2,ang2,x3,y3,ang3)
    generapunto(x,y)
    if error<resultado[2]:
        resultado=[]
        resultado.append(x)
        resultado.append(y)
        resultado.append(error)
if ang4<>9999:
    x,y,error=haceelcruce(x1,y1,ang1,x4,y4,ang4)
    generapunto(x,y)
    if error<resultado[2]:
        resultado=[]
        resultado.append(x)
        resultado.append(y)
        resultado.append(error)
    x,y,error=haceelcruce(x2,y2,ang2,x4,y4,ang4)
    generapunto(x,y)
    if error<resultado[2]:
        resultado=[]
        resultado.append(x)
        resultado.append(y)
        resultado.append(error)
    x,y,error=haceelcruce(x3,y4,ang3,x4,y4,ang4)
    generapunto(x,y)
    if error<resultado[2]:
        resultado=[]
        resultado.append(x)
        resultado.append(y)
        resultado.append(error)  

#hago una nueva capa con el mejor resultado
x,y,error=resultado[0],resultado[1],resultado[2]
# create layer
vl2 = QgsVectorLayer("Point", "MejorResultado", "memory")
pr2 = vl2.dataProvider()
vl2.startEditing()
# add fields
pr2.addAttributes([QgsField("error", QVariant.Int),
                    QgsField("x",  QVariant.Int),
                    QgsField("y", QVariant.Double)])
vl2.updateFields() 
# tell the vector layer to fetch changes from the provider
print "ok creados los campos"
# add a feature
fet = QgsFeature()
fet.setGeometry(QgsGeometry.fromPoint(QgsPoint(x,y)))
fet.setAttributes([error, x, y])
pr2.addFeatures([fet])
#cambio la simbologia
symbol = QgsMarkerSymbolV2.createSimple({'name': 'circle', 'color': 'red','size': '10',})
vl2.rendererV2().setSymbol(symbol)

# update layer's extent when new features have been added
# because change of extent in provider is not propagated to the layer
vl2.updateExtents()
vl2.commitChanges()
vl2.updateExtents()
canvas = qgis.utils.iface.mapCanvas()
canvas.setExtent(vl.extent())
#meto las capas en el mapa
QgsMapLayerRegistry.instance().addMapLayer(vl)
QgsMapLayerRegistry.instance().addMapLayer(vl2)
#app.exec_()














