from time import sleep
import pyautogui

#Juego Encontrar Pares Tablero 3x6
game_rows=3
game_columns=6 #only even numbers // solo numeros pares permitidos

#Card Images
carta_01 = '01.png'
carta_02 = '02.png'
carta_03 = '03.png'
carta_04 = '04.png'
carta_05 = '05.png'
carta_06 = '06.png'
carta_07 = '07.png'
carta_08 = '08.png'

#x_inicial, Yinial, X_final, Y_final
inicio_carta_coordenada = [502, 333, 656, 513] #card dimensions



def find_average_coordinates(image_path, confidence=0.9, threshold_distance=10):
    # Find all occurrences of the image on the screen
    matches = list(pyautogui.locateAllOnScreen(image_path, confidence=confidence))

    # Use a list to store groups of coordinates
    coordinate_groups = []

    # Group coordinates that are close to each other
    for match in matches:
        coordinate = (match.left, match.top)

        grouped = False
        for group in coordinate_groups:
            if any(abs(coordinate[0] - existing_coord[0]) < threshold_distance and
                   abs(coordinate[1] - existing_coord[1]) < threshold_distance
                   for existing_coord in group):
                group.append(coordinate)
                grouped = True
                break

        if not grouped:
            coordinate_groups.append([coordinate])

    # Calculate and return the rounded average coordinates for each group
    average_coordinates = []
    for group in coordinate_groups:
        x_avg = round(sum(coord[0] for coord in group) / len(group))
        y_avg = round(sum(coord[1] for coord in group) / len(group))
        average_coordinates.append((x_avg, y_avg))

    return average_coordinates

class Carta:
    def __init__(self, id, x, y, ancho, largo):
        self.id = id
        self.x = x
        self.y = y
        self.ancho = ancho
        self.largo = largo
        self.estado = "Reverso"
    
    def getEstado(self):
        return self.estado
    
    def coord_center(self):
        centro_x = self.x + self.ancho // 2
        centro_y = self.y + self.largo // 2

        pyautogui.click(centro_x,centro_y)
        return centro_x, centro_y

    def identify_card(self):
        times=0

        while self.estado == "Reverso" or times > 3:

            for i in range(1, 10):
                
                template = f'{i:02d}.png'                
                
                if pyautogui.locateOnScreen(template,region=(self.x, self.y, self.ancho, self.largo) , confidence=0.7):
                    self.estado = str(i)
                    print(f"Carta {self.id} identificada. Estado: {self.estado}")
            times+=1
                        
  

class Tablero:
    def __init__(self):
        x1, y1, x2, y2 = inicio_carta_coordenada
        ancho_carta = x2 - x1
        largo_carta = y2 - y1
        self.cartas = {(fila + 1, columna + 1): Carta(f"{fila + 1}{columna + 1}",
                      x1 + columna * ancho_carta, y1 + fila * largo_carta, ancho_carta, largo_carta)
                       for fila in range(game_rows) for columna in range(game_columns)}
    
    

def check_and_click_matching_states(tablero,rowP,colP):
    # Dictionary to store the states and corresponding card coordinates
    state_coordinates = {}

    # Iterate through all cards on the board
    for row in range(1, rowP+1):
        for col in range(1, colP+1):
            carta = tablero.cartas[row, col]
            estado = carta.getEstado()

            # Ignore cards in "Reverso" state
            if estado != "Reverso":
                if estado not in state_coordinates:
                    # Store the first occurrence of the state
                    state_coordinates[estado] = [(row, col)]
                else:
                    # Found a matching state, click on the cards
                    coordinates_list = state_coordinates[estado]
                    coordinates_list.append((row, col))

                    for coordinates in coordinates_list:
                        x, y = tablero.cartas[coordinates].coord_center()
                        pyautogui.click(x, y)
                        sleep(0.1)

                    # Change the state of the clicked cards back to "Reverso"
                    for coordinates in coordinates_list:
                        tablero.cartas[coordinates].estado = "Reverso"

                    # Remove the state from the dictionary to avoid double-clicking
                    del state_coordinates[estado]
       


tablero = Tablero()

input("Press Enter to Start /")

for r in range(1,game_rows+1):
    for c in range(1, game_columns, 2):
        pyautogui.click(tablero.cartas[r,c].coord_center())
        pyautogui.click(tablero.cartas[r,c+1].coord_center())

        tablero.cartas[r,c].identify_card()
        tablero.cartas[r,c+1].identify_card()

        check_and_click_matching_states(tablero,r,c+1)
        
