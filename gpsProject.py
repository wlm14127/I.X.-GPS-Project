#imported libraries
from gps import *
from tkinter import Tk, Canvas, Entry
from tkinter import *
from tkintermapview import TkinterMapView

#######################################################################################################################################################################################
#functions


# makes the bevelled rectangles
def round_rectangle(x1, y1, x2, y2, radius=25, **kwargs):
        
    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]

    return canvas.create_polygon(points, **kwargs, smooth=True)

#creates a path when you click on a charging station
def marker_click(marker):
    path_1 = map_widget.set_path([marker_1.position, marker.position], command=path_click, color='black')

#deletes the created path when you click on it
def path_click(path):
    path.delete()

#updates the listbox as you type in the search bar
def update_listbox(*args):
    search_term = search_var.get()
    listbox.delete(0, END)
    for item in all_items:
        if search_term.lower() in item.lower():
            listbox.insert(END, item)

#sends you to the charging station that you click on
def items_selected(event):
    selected_indicies = listbox.curselection()
    selected_langs = ','.join([listbox.get(i) for i in selected_indicies])
    for i in range(79):
        if selected_langs == markers[i][0]:
            map_widget.set_position(markers[i][1], markers[i][2])
            map_widget.set_zoom(15)
            
#######################################################################################################################################################################################
#main code

gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)

#checks gps for a signal
#if one is not found, it just makes the values of latitude, longitude and speed unknown
valid = True
while valid == True:
    nx = gpsd.next()
    if nx['class'] == 'TPV':
        latitude = getattr(nx, 'lat', "Unknown")
        longitude = getattr(nx, 'lon', "Unknown")
        speed =  str(getattr(nx,'speed','nan'))
        print("Your position: lon = " + str(longitude) + ", lat = " + str(latitude))
        valid = False


#creates the tkinter window
root = Tk()
root.geometry(f"{2000}x{2000}")
root.title("IX GPS map.py")
canvas = Canvas(root, width=1250, height=1000, bg='black')
canvas.pack()

#offline map
script_directory = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(script_directory, 'offlineMap.db')

#creates and places the tkinter map
my_rectangle = round_rectangle(15, 25, 760, 675, radius=20, fill="grey9")
map_widget = TkinterMapView(canvas, width=715, height=620, corner_radius=0, database_path=database_path)
map_widget.pack(fill="both", expand=True)
map_widget.place(relx=0.31, rely=0.35, anchor='center')
#sets location to Chelmsford if one is unknown
map_widget.fit_bounding_box((51.745446, 0.455074),(51.727586, 0.492480))
map_widget.set_zoom(12)

my_rectangle = round_rectangle(775, 25, 1235, 975, radius=20, fill="grey9")
canvas.create_text(1000 , 400, text="Latitude: " + str(latitude), fill="white", font=('Helvetica 30 bold'))
canvas.create_text(1005, 450, text="Longitude: " + str(longitude), fill="white", font=('Helvetica 30 bold'))
canvas.create_text(1005, 500, text="Speed: " + str(speed) + " mph", fill="white", font=('Helvetica 30 bold'))

canvas.create_text(400, 775, text="I.X. Electric", fill="white", font=('Roman 60 bold'))
canvas.create_text(400, 875, text="Charger Finder", fill="white", font=('Roman 60 bold'))
canvas.create_text(1005, 600, text="Your Location", fill="red", font=('Helvetica 30 bold'))
canvas.create_text(1005, 650, text="Charging Stations", fill="green", font=('Helvetica 30 bold'))

#creates search box
search_var = StringVar()
search_var.trace('w', update_listbox)
searchbox = Entry(canvas, textvariable=search_var)
searchbox.pack()
searchbox.place(relx=0.8, rely=0.053, anchor='center')

#creates a listbox with each of the different electric charging stations in it
listbox = Listbox(canvas)
for i in ['Tesla Supercharger', 'Chargemaster', 'GeniePoint', 'ElectricBlue', 'bp pulse', 'VIRTA', 'PodPoint', 'Shell Recharge', 'British Gas', 'Osprey', 'Vehicle', 'Electric Vehicle', 'has.to.be', 'Public', 'Porsche Destination', 'EB Charging', 'ChargePoint', 'ESB escars', 'GRIDSERVE', 'InstaVolt', 'be.ENERGISED']:
    listbox.insert(END, i)
listbox.pack()
listbox.place(relx=0.8, rely=0.17, anchor='center')
all_items = listbox.get(0, END)
listbox.bind('<<ListboxSelect>>', items_selected)

#only creates a marker for the user is the location is known
if longitude != 'Unknown' and latitude != 'Unkown':
    marker_1 = map_widget.set_position(latitude, longitude, marker=True)
    print(marker_1.position)

#######################################################################################################################################################################################

#creates a marker for each charging station and puts it in a 2D list
marker_2 = map_widget.set_marker(51.754843, 0.447273, text='GeniePoint', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_3 = map_widget.set_marker(51.743783, 0.471797, text='Chargemaster', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_4 = map_widget.set_marker(51.750370, 0.511401, text='Tesla Supercharger', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_5 = map_widget.set_marker(51.75164, 0.508905, text='ElectricBlue', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_6 = map_widget.set_marker(51.740488, 0.498761, text='bp pulse', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_7 = map_widget.set_marker(51.735801, 0.464730, text='bp pulse', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_8 = map_widget.set_marker(51.734014, 0.468737, text='VIRTA', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_9 = map_widget.set_marker(51.758952, 0.453777, text='Chargemaster', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_10 = map_widget.set_marker(51.730004, 0.466721, text='ElectricBlue', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_11 = map_widget.set_marker(51.728282, 0.468528, text='bp pulse', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_12 = map_widget.set_marker(51.734323, 0.477432, text='PodPoint', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_13 = map_widget.set_marker(51.731927, 0.477818, text='bp pulse', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_14 = map_widget.set_marker(51.729588, 0.478310, text='Chargemaster', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_15 = map_widget.set_marker(51.778703, 0.489578, text='Electric Blue', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_16 = map_widget.set_marker(51.720932, 0.525906, text='Chargemaster', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_17 = map_widget.set_marker(51.709146, 0.507768, text='Tesla Supercharger', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_18 = map_widget.set_marker(51.643442, 0.618136, text='Chargemaster', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_19 = map_widget.set_marker(51.651490, 0.596301, text='Chargemaster', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_20 = map_widget.set_marker(51.654762, 0.604351, text='PodPoint', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_21 = map_widget.set_marker(51.596200, 0.586042, text='bp pulse', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_22 = map_widget.set_marker(51.578398, 0.599876, text='Shell Recharge', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_23 = map_widget.set_marker(51.554649, 0.605342, text='GeniePoint', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_24 = map_widget.set_marker(51.552271, 0.611879, text='PodPoint', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_25 = map_widget.set_marker(51.561186, 0.683508, text='PodPoint', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_26 = map_widget.set_marker(51.558322, 0.696134, text='Shell Recharge', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_27 = map_widget.set_marker(51.541689, 0.695525, text='GeniePoint', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_28 = map_widget.set_marker(51.542410, 0.695394, text='GeniePoint', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_29 = map_widget.set_marker(51.540155, 0.709013, text='British Gas', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_30 = map_widget.set_marker(51.535140, 0.717290, text='GeniePoint', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_31 = map_widget.set_marker(51.534129, 0.716036, text='PodPoint', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_32 = map_widget.set_marker(51.530127, 0.784957, text='PodPoint', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_33 = map_widget.set_marker(51.615177, 0.519939, text='Chargemaster', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_34 = map_widget.set_marker(51.590673, 0.519939, text='Osprey', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_35 = map_widget.set_marker(51.586421, 0.518723, text='Vehicle', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_36 = map_widget.set_marker(51.590988, 0.476235, text='PodPoint', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_37 = map_widget.set_marker(51.579628, 0.449340, text='Electric Vehicle', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_38 = map_widget.set_marker(51.568719, 0.453111, text='has.to.be', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_39 = map_widget.set_marker(51.563154, 0.502404, text='PodPoint', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_40 = map_widget.set_marker(51.523569, 0.555195, text='PodPoint', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_41 = map_widget.set_marker(51.515672, 0.426257, text='Public', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_42 = map_widget.set_marker(51.655582, 0.356900, text='Porsche Destination', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_43 = map_widget.set_marker(51.647970, 0.386423, text='EB Charging', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_44 = map_widget.set_marker(51.630399, 0.411805, text='ChargePoint', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_45 = map_widget.set_marker(51.619141, 0.306873, text='Osprey', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_46 = map_widget.set_marker(51.648897, 0.267447, text='Chargemaster', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_47 = map_widget.set_marker(51.602324, 0.243887, text='ESB escars', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_48 = map_widget.set_marker(51.597208, 0.219560, text='Chargemaster', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_49 = map_widget.set_marker(51.580263, 0.239758, text='Chargemaster', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_50 = map_widget.set_marker(51.563487, 0.216169, text='PodPoint', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_51 = map_widget.set_marker(51.555833, 0.251030, text='Shell Recharge', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_52 = map_widget.set_marker(51.573666, 0.182074, text='PodPoint', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_53 = map_widget.set_marker(51.728718, 0.680270, text='Public', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_54 = map_widget.set_marker(51.735389, 0.680308, text='PodPoint', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_55 = map_widget.set_marker(51.736951, 0.677848, text='PodPoint', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_56 = map_widget.set_marker(51.796446, 0.632374, text='bp pulse', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_57 = map_widget.set_marker(51.796711, 0.634156, text='PodPoint', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_58 = map_widget.set_marker(51.797252, 0.636088, text='bp pulse', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_59 = map_widget.set_marker(51.800496, 0.638443, text='bp pulse', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_60 = map_widget.set_marker(51.805678, 0.639752, text='Chargemaster', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_61 = map_widget.set_marker(51.806507, 0.639730, text='bp pulse', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_62 = map_widget.set_marker(51.807963, 0.638200, text='bp pulse', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_63 = map_widget.set_marker(51.852579, 0.521782, text='GRIDSERVE', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_64 = map_widget.set_marker(51.852638, 0.522437, text='Tesla Supercharger', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_65 = map_widget.set_marker(51.857631, 0.521873, text='PodPoint', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_66 = map_widget.set_marker(51.857260, 0.516857, text='bp pulse', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_67 = map_widget.set_marker(51.865725, 0.520343, text='Shell Recharge', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_68 = map_widget.set_marker(51.867348, 0.581596, text='InstaVolt', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_69 = map_widget.set_marker(51.875509, 0.555008, text='bp pulse', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_70 = map_widget.set_marker(51.878153, 0.562174, text='PodPoint', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_71 = map_widget.set_marker(51.877801, 0.554113, text='bp pulse', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_72 = map_widget.set_marker(51.877440, 0.552063, text='PodPoint', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_73 = map_widget.set_marker(51.878559, 0.550040, text='ChargeYourCar', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_74 = map_widget.set_marker(51.888852, 0.538199, text='InstaVolt', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_75 = map_widget.set_marker(51.748505, 0.402674, text='Porsche Destination', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_76 = map_widget.set_marker(51.871230, 0.368020, text='be.ENERGISED', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_77 = map_widget.set_marker(51.871823, 0.334499, text='bp pulse', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_78 = map_widget.set_marker(51.872313, 0.362707, text='bp pulse', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_79 = map_widget.set_marker(51.872283, 0.361096, text='bp pulse', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)
marker_80 = map_widget.set_marker(51.873128, 0.346305, text='PodPoint', marker_color_circle='Green', marker_color_outside='Green4', text_color='Green', command=marker_click)

markers = [['GeniePoint', 51.754843, 0.447273], ['Chargemaster', 51.743783, 0.471797], ['Tesla Supercharger', 51.750370, 0.511401], ['ElectricBlue', 51.75164, 0.508905],
           ['bp pulse', 51.740488, 0.498761], ['bp pulse', 51.735801, 0.464730], ['VIRTA', 51.734014, 0.468737], ['Chargemaster', 51.758952, 0.453777],
           ['ElectricBlue', 51.730004, 0.466721], ['bp pulse', 51.728282, 0.468528], ['PodPoint', 51.734323, 0.477432], ['bp pulse', 51.731927, 0.477818],
           ['Chargemaster', 51.729588, 0.478310], ['Electric Blue', 51.778703, 0.489578], ['Chargemaster', 51.720932, 0.525906], ['Tesla Supercharger', 51.709146, 0.507768],
           ['Chargemaster', 51.643442, 0.618136], ['Chargemaster', 51.651490, 0.596301], ['PodPoint', 51.654762, 0.604351], ['bp pulse', 51.596200, 0.586042],
           ['Shell Recharge', 51.578398, 0.599876], ['GeniePoint', 51.554649, 0.605342], ['PodPoint', 51.552271, 0.611879], ['PodPoint', 51.561186, 0.683508],
           ['Shell Recharge', 51.558322, 0.696134], ['GeniePoint', 51.541689, 0.695525], ['GeniePoint', 51.542410, 0.695394], ['British Gas', 51.540155, 0.709013],
           ['GeniePoint', 51.535140, 0.717290], ['PodPoint', 51.534129, 0.716036], ['PodPoint', 51.530127, 0.784957], ['Chargemaster', 51.615177, 0.519939],
           ['Osprey', 51.590673, 0.519939], ['Vehicle', 51.586421, 0.518723], ['PodPoint', 51.590988, 0.476235], ['Electric Vehicle', 51.579628, 0.449340],
           ['has.to.be', 51.568719, 0.453111], ['PodPoint', 51.563154, 0.502404], ['PodPoint', 51.523569, 0.555195], ['Public', 51.515672, 0.426257],
           ['Porsche Destination', 51.655582, 0.356900], ['EB Charging', 51.647970, 0.386423], ['Osprey', 51.619141, 0.306873], ['Chargemaster', 51.648897, 0.267447],
           ['Chargemaster', 51.648897, 0.267447], ['ESB escars', 51.602324, 0.243887], ['Chargemaster', 51.597208, 0.219560], ['Chargemaster', 51.580263, 0.239758],
           ['PodPoint', 51.563487, 0.216169], ['Shell Recharge', 51.555833, 0.251030], ['PodPoint', 51.573666, 0.182074], ['Public', 51.728718, 0.680270],
           ['PodPoint', 51.735389, 0.680308], ['PodPoint', 51.736951, 0.677848], ['bp pulse', 51.796446, 0.632374], ['PodPoint', 51.796711, 0.634156],
           ['bp pulse', 51.797252, 0.636088], ['bp pulse', 51.800496, 0.638443], ['Chargemaster', 51.805678, 0.639752], ['bp pulse', 51.806507, 0.639730],
           ['bp pulse', 51.807963, 0.638200], ['GRIDSERVE', 51.852579, 0.521782], ['Tesla Supercharger', 51.852638, 0.522437], ['PodPoint', 51.857631, 0.521873],
           ['bp pulse', 51.857260, 0.516857], ['Shell Recharge', 51.865725, 0.520343], ['InstaVolt', 51.867348, 0.581596],['bp pulse', 51.875509, 0.555008],
           ['PodPoint', 51.878153, 0.562174], ['bp pulse', 51.877801, 0.554113], ['PodPoint', 51.877440, 0.552063], ['ChargeYourCar', 51.878559, 0.550040],
           ['InstaVolt', 51.888852, 0.538199], ['Porsche Destination', 51.748505, 0.402674], ['be.ENERGISED', 51.871230, 0.368020], ['bp pulse', 51.871823, 0.334499],
           ['bp pulse', 51.872313, 0.362707], ['bp pulse', 51.872283, 0.361096], ['PodPoint', 51.873128, 0.346305]]

root.mainloop()