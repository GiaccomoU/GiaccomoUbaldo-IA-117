import java.util.ArrayList;

public class Graph {
	public final static int NODO_BASE = 0;
	public final static int PRIMER_NODO_EN_COLA = 0;
	public final static int NODO_DESTINO = 1;
	public final static int DISTANCIA_ENTRE_DOS_NODOS = 6;
	public final static int MAX_INT = 1000000;
	
	ArrayList<Node> nodos;
	int idNodoInicial;
	
	public Graph(int cantNodos, ArrayList<ArrayList<Integer>> conexiones, int pIdNodoInicial){
		idNodoInicial = pIdNodoInicial;
		this.nodos = new ArrayList<Node>();
		for(int i = 1; i < cantNodos+1; i++){
			Node nuevoNodo = new Node(i);
			this.nodos.add(nuevoNodo);
		}
		assignConnections(this.nodos, conexiones);
	}
	
	public Node getNodeById(int pId){
		for(int i = 0; i < nodos.size(); i++){
			if(nodos.get(i).id == pId){
				return nodos.get(i);
			}
		}
		System.out.println("No se encontró el nodo indicado.");
		return null;
	}
	
	public void assignConnections(ArrayList<Node> listaDeNodos, ArrayList<ArrayList<Integer>> conexiones){
		for(int i = 0; i < listaDeNodos.size(); i++){
			ArrayList<Integer> listaDeConexiones = new ArrayList<Integer>();
			int idActual = listaDeNodos.get(i).getId();
			
			for(int j = 0; j < conexiones.size(); j++){
				if(conexiones.get(j).get(NODO_BASE) == idActual){
					listaDeConexiones.add(conexiones.get(j).get(NODO_DESTINO));
				}else if(conexiones.get(j).get(NODO_DESTINO) == idActual){
					listaDeConexiones.add(conexiones.get(j).get(NODO_BASE));
				}
			}
			listaDeNodos.get(i).setVecinos(listaDeConexiones);
		}
	}
	
	public boolean nodoEstaExplorado(int id, ArrayList<Integer> nodosExplorados){
		if(nodosExplorados.contains(id)){
			return true;
		}else{
			return false;
		}
	}
	
	public String toString(){
		String str = "";
		str += "Cantidad de nodos: " + this.nodos.size() + "\n";
		str += "Nodo inicial: " + this.idNodoInicial + "\n";
		str += "Conexiones:\n";
		for(int i = 0; i < this.nodos.size(); i++){
			str += this.nodos.get(i).toString();
		}
		return str;
	}
}
