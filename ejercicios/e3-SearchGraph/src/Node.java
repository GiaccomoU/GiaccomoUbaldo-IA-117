import java.util.ArrayList;

public class Node{
    int id;
    ArrayList<Integer> vecinos;
    
    public Node(int pId){
    	id = pId;
    	vecinos = new ArrayList<Integer>();
    }
    
    public Node(int pId, ArrayList<Integer> pVecinos){
    	id = pId;
    	vecinos = pVecinos;
    }

	public int getId() {
		return id;
	}

	public void setId(int id) {
		this.id = id;
	}

	public ArrayList<Integer> getVecinos() {
		return vecinos;
	}

	public void setVecinos(ArrayList<Integer> vecinos) {
		this.vecinos = vecinos;
	}
    
	public String toString(){
		String str = "";
		str += "Nodo ID: " + this.id + "\n";
		str += "Vecinos: ";
		for(int i = 0; i < vecinos.size(); i++){
			str += vecinos.get(i) + "  ";
		}
		str += "\n";
		return str;
	}
	
}
