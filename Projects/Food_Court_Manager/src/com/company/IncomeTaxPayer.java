package com.company;

public abstract class IncomeTaxPayer {

    private static int currentMaxTaxID;
    private int taxID;
    private String name;
    double income;

    public IncomeTaxPayer(String name){
        this.name = name;
        this.taxID = currentMaxTaxID;
        currentMaxTaxID++;
    }

    public static int getCurrentMaxTaxID() {
        return currentMaxTaxID;
    }

    public int getTaxID() {
        return taxID;
    }

    public String getName() {
        return name;
    }

    public double getIncome() {
        return this.income;
    }

    public void setIncome(double income) {
        this.income = income;
    }

    public String toString() {
        return "  " + taxID + " " + name + " income " + income ;
    }

    public boolean equals(Object obj) {
        boolean right_type = (obj instanceof IncomeTaxPayer);
        boolean right_ID = ((IncomeTaxPayer) obj).getTaxID() == this.getTaxID();
        boolean equality = right_type && right_ID;
        return equality;
    }

    public abstract double calculateIncomeTax();
}
