package com.company;



public class Owner extends IncomeTaxPayer {

    final private int incomeTaxPct = 10;
    private double salaryExpenses;

    private FoodPlace foodPlace;

    public Owner(String name) {
        super(name);
    }

    public FoodPlace getFoodPlace(){
        return foodPlace;
    }

    public int getIncomeTaxPct() {
        return incomeTaxPct;
    }

    public double getSalaryExpenses() {
        return salaryExpenses;
    }

    public void setSalaryExpenses(double salaryExpenses) {
        this.salaryExpenses = salaryExpenses;
    }

    public void setFoodPlace(FoodPlace foodPlace) {
        this.foodPlace = foodPlace;
    }

    @Override
    public double calculateIncomeTax() {

        double incomeTax = (0.10)*(this.getIncome() - this.getSalaryExpenses() - foodPlace.getFixedCosts());
        if (incomeTax < 0) {
            return 0;
        }
        return incomeTax;
    }
}
