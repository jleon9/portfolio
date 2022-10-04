package com.company;

import java.util.ArrayList;
import java.util.List;


public class TaxCollector {

    private List<FoodPlace> foodPlaces = new ArrayList<>();

    private double incomeTaxCollected;
    private double salesTaxCollected;

    public TaxCollector(List<FoodPlace> foodPlaces) {
        this.foodPlaces = foodPlaces;
    }

    public List<FoodPlace> getFoodPlaces() {
        return foodPlaces;
    }

    public double getIncomeTaxCollected() {
        return incomeTaxCollected;
    }

    public double getSalesTaxCollected() {
        return salesTaxCollected;
    }

    public void collectTax() {
        double CIT = 0; // Collected Income Tax
        double CST = 0; // Collected Sales Tax

        for (FoodPlace FP : this.foodPlaces) {

            CST += FP.getTotalSalesTax();
            List<IncomeTaxPayer> LTP = FP.getIncomeTaxPayers(); // List of Tax Payers

            for (IncomeTaxPayer ITP : LTP) {
                CIT += ITP.calculateIncomeTax();
            }
        }

        this.incomeTaxCollected = CIT;
        this.salesTaxCollected = CST;

    }

    public String toString() {
        return "TaxCollector: income tax collected: " + incomeTaxCollected + ", sales tax collected: " + salesTaxCollected;
    }

}
