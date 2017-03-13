import java.io.*;
import java.util.*;

public class Solution {
	
	public static Graph leerGrafo(BufferedReader br) throws IOException{
		String cantNodosYVertices = br.readLine();
        String[] cantidadesSeparadas = cantNodosYVertices.split(" ");
        
        int cantNodos = Integer.parseInt(cantidadesSeparadas[0]);
        int cantVertices = Integer.parseInt(cantidadesSeparadas[1]);
        ArrayList<ArrayList<Integer>> listaConexiones = new ArrayList<ArrayList<Integer>>();
        
        for(int i = 0; i < cantVertices; i++){
        	String strConexion = br.readLine();
        	String[] conexionPartida = strConexion.split(" ");
        	ArrayList<Integer> conexion = new ArrayList<Integer>();
        	conexion.add(Integer.parseInt(conexionPartida[0]));
        	conexion.add(Integer.parseInt(conexionPartida[1]));
        	listaConexiones.add(conexion);
        }
        
        int nodoInicial = Integer.parseInt(br.readLine());
       
        
        Graph nuevoGrafo = new Graph(cantNodos, listaConexiones, nodoInicial);
        //System.out.print(nuevoGrafo.toString());
        return nuevoGrafo;
	}

	public static void printArray(ArrayList<Integer> arreglo){
		System.out.print("[");
		for(int i = 0; i < arreglo.size(); i++){
			System.out.print(arreglo.get(i));
			if(i != arreglo.size()-1){
				System.out.print(", ");
			}
		}
		System.out.println("]");
	}
	
	public static ArrayList<Integer> analizar(Graph grafo){
		ArrayList<Integer> distanciasFinales = new ArrayList<Integer>();
		for(int i = 1; i <= grafo.nodos.size(); i++){
			if(i != grafo.idNodoInicial){
				int distancia = 0;
				ArrayList<Integer> nodosExplorados = new ArrayList<Integer>();
				ArrayList<Integer> nodosEnCola = new ArrayList<Integer>();
				ArrayList<Integer> nodosVecinos = new ArrayList<Integer>();
				
				nodosEnCola.add(grafo.idNodoInicial);
				int nodoObjetivo = i;
				boolean seEncontroObjetivo = false;
				
				while(!seEncontroObjetivo){
					
					//Agregar contenido de COLA a EXPLORADOS
					for(int j = 0; j < nodosEnCola.size(); j++){
						nodosExplorados.add(nodosEnCola.get(j));
					}

					//Agregar los vecinos de los nodos en cola a VECINOS si no están en EXPLORADOS
					for(int k = 0; k < nodosEnCola.size(); k++){
						ArrayList<Integer> vecinosDeNodoActual = grafo.getNodeById(nodosEnCola.get(k)).vecinos;
						
						for(int m = 0; m < vecinosDeNodoActual.size(); m++){
							if(!nodosExplorados.contains(vecinosDeNodoActual.get(m))){
								nodosVecinos.add(vecinosDeNodoActual.get(m));
							}	
						}
					}
					distancia += 6;
					
					if(nodosVecinos.isEmpty()){
						distancia = -1;
						distanciasFinales.add(distancia);
						seEncontroObjetivo = true;
					}
					
					for(int p = 0; p < nodosVecinos.size(); p++){
						if(nodosVecinos.get(p) == nodoObjetivo){
							distanciasFinales.add(distancia);
							seEncontroObjetivo = true;
						}
					}
					nodosEnCola.clear();
					for(int z = 0; z < nodosVecinos.size(); z++){
						nodosEnCola.add(nodosVecinos.get(z));
					}
					//nodosEnCola = nodosVecinos;
					nodosVecinos.clear();
				}
				
			}
		}
		
		return distanciasFinales;
	}
	
    public static void main(String[] args){
    	ArrayList<Graph> listaGrafos = new ArrayList<Graph>();
    	
    	System.out.println("Inserte los valores en el formato indicado:");
    	
    	BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    	try {
			int cantProblemas = Integer.parseInt(br.readLine());
            //System.out.println(cantProblemas);
			for(int i = 0; i < cantProblemas; i++){
				listaGrafos.add(leerGrafo(br));
			}
            
		} catch (Exception e) {
			e.printStackTrace();
		} 
    	
    	ArrayList<ArrayList<Integer>> listaDistancias = new ArrayList<ArrayList<Integer>>();
    	
    	for(int i = 0; i < listaGrafos.size(); i++){
    		if(listaGrafos.get(i) != null){
    			listaDistancias.add(analizar(listaGrafos.get(i)));
    		}else{
    			System.out.println("Es nulo");
    		}
    	}
    	
    	for(int q = 0; q < listaDistancias.size(); q++){
    		for(int r = 0; r < listaDistancias.get(q).size(); r++){
        		System.out.print(listaDistancias.get(q).get(r));
        		System.out.print(" ");
        	}
    		System.out.print("\n");
    	}
    	
    	//System.out.print("La cantidad de distancias resultantes es: ");
    	//System.out.print(listaDistancias.size());
    	
    }
}