package com.company;
import java.util.ArrayList;
import java.util.HashMap;

public class ERPriorityQueue{

    public ArrayList<Patient>  patients;
    public HashMap<String,Integer>  nameToIndex;

    public ERPriorityQueue(){

        //  use a dummy node so that indexing starts at 1, not 0

        patients = new ArrayList<Patient>();
        patients.add( new Patient("dummy", 0.0) );

        nameToIndex  = new HashMap<String,Integer>();
    }

    private int parent(int i){
        return i/2;
    }

    private int leftChild(int i){
        return 2*i;
    }

    private int rightChild(int i){
        return 2*i+1;
    }

    /*
    TODO: OPTIONAL
    TODO: Additional helper methods such as isLeaf(int i), isEmpty(), swap(int i, int j) could be useful for this assignment
     */

    void swap(int i, int j) {

        Patient tmp = patients.get(i);

        patients.set(i, patients.get(j));
        patients.set(j, tmp);

        nameToIndex.put(patients.get(i).name, i);
        nameToIndex.put(patients.get(j).name, j);
    }


    public void upHeap(int i){
        // TODO: Implement your code here

        //int j = i;

        while (i > 1 && patients.get(i).getPriority() < patients.get(i/2).getPriority()) {
            swap(i, i/2);
            i = i/2;
        }

    }

    public void downHeap(int i){
        // TODO: Implement your code here

        int child;
        while (2*i < patients.size()) {
            child = 2*i;
            if (child+1 < patients.size()) {

                if (patients.get(child+1).getPriority() < patients.get(child).getPriority()) {
                    child++;
                }
            }

            if (patients.get(child).getPriority() < patients.get(i).getPriority()) {

                swap(i, child);
                i = child;
            }
            else return;
        }
    }



    public boolean contains(String name){
        // TODO: Implement your code here & remove return statement

        boolean isInside = nameToIndex.containsKey(name);

        return isInside;
    }

    public double getPriority(String name){
        // TODO: Implement your code here & remove return statement

        int index = nameToIndex.get(name);
        if (!contains(name)) {
            return -1;
        }

        return patients.get(index).getPriority();
    }

    public double getMinPriority(){
        // TODO: Implement your code here & remove return statement
        if (patients.size() == 1) return -1;
        return patients.get(1).priority;
    }

    public String removeMin(){
        // TODO: Implement your code here & remove return statement
        if (patients.size() == 1) return null;
        String lowest_name = patients.get(1).name;
        this.remove(lowest_name);
        return lowest_name;




    }

    public String peekMin(){
        // TODO: Implement your code here & remove return statement

        if (patients.size() == 1) return null;

        return patients.get(1).name;
    }

    /*
     * There are two add methods.  The first assumes a specific priority.
     * The second gives a default priority of Double.POSITIVE_INFINITY
     *
     * If the name is already there, then return false.
     */

    public boolean  add(String name, double priority){
        // TODO: Implement your code here & remove return statement
        if (contains(name)) return false;
        Patient P = new Patient(name, priority);
        patients.add(P);
        upHeap(patients.size()-1);
        nameToIndex.put(name, patients.indexOf(P));
        return true;
    }

    public boolean  add(String name){
        // TODO: Implement your code here
        return add(name, Double.POSITIVE_INFINITY);
    }

    public boolean remove(String name){
        // TODO: Implement your code here
        if (patients.size() <= 1 || !contains(name)) return false;

        int pIndex = nameToIndex.get(name);
        int size = patients.size()-1;

        swap(pIndex, size);
        patients.remove(size);
        nameToIndex.remove(name);
        if (pIndex < patients.size()) {
            upHeap(pIndex);
        }
        downHeap(pIndex);


        return true;
    }

    /*
     *   If new priority is different from the current priority then change the priority
     *   (and possibly modify the heap).
     *   If the name is not there, return false
     */

    public boolean changePriority(String name, double priority){
        // TODO: Implement your code here & remove return statement

        if (!contains(name)) return false;
        int dp_Index = nameToIndex.get(name);
        patients.get(dp_Index).priority = priority;
        upHeap(dp_Index);
        downHeap(dp_Index);
        return true;
    }

    public ArrayList<Patient> removeUrgentPatients(double threshold){
        // TODO: Implement your code here & remove return statement

        ArrayList<Patient> patientsC = new ArrayList<>(patients);
        ArrayList<Patient> UPatient = new ArrayList<Patient>();
        patientsC.remove(0);

        for (Patient P : patientsC) {
            if (P.priority <= threshold) {
                //int pIndex = nameToIndex.get(P.name);
                UPatient.add(P);
                this.remove(P.name);
            }
        }

        return UPatient;


    }

    public ArrayList<Patient> removeNonUrgentPatients(double threshold){
        // TODO: Implement your code here & remove return statement
        ArrayList<Patient> patientsC = new ArrayList<>(patients);
        ArrayList<Patient> UPatient = new ArrayList<Patient>();
        patientsC.remove(0);

        for (Patient P : patientsC) {
            if (P.priority >= threshold) {
                //int pIndex = nameToIndex.get(P.name);
                UPatient.add(P);
                this.remove(P.name);
            }
        }

        return UPatient;
    }

    static class Patient{
        private String name;
        private double priority;

        Patient(String name,  double priority){
            this.name = name;
            this.priority = priority;
        }

        Patient(Patient otherPatient){
            this.name = otherPatient.name;
            this.priority = otherPatient.priority;
        }

        double getPriority() {
            return this.priority;
        }

        void setPriority(double priority) {
            this.priority = priority;
        }

        String getName() {
            return this.name;
        }

        @Override
        public String toString(){
            return this.name + " - " + this.priority;
        }

        public boolean equals(Object obj){
            if (!(obj instanceof  ERPriorityQueue.Patient)) return false;
            Patient otherPatient = (Patient) obj;
            return this.name.equals(otherPatient.name) && this.priority == otherPatient.priority;
        }

    }

}