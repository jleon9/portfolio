package com.company;


public class Customer  {

    private String name;
    private int  targetTipPct;

    public Customer(String name, int targetTipPct) {
        this.name = name;
        this.targetTipPct = targetTipPct;
    }

    public String getName() {
        return name;
    }

    public int getTargetTipPct() {
        return targetTipPct;
    }

    public String getDescriptiveMessage(FoodPlace foodPlace) {
        return this.name + " dined in " + foodPlace.getName();
    }

    public void dineAndPayCheck(FoodPlace foodPlace, double menuPrice ) {

        Check bill = new Check(menuPrice);
        bill.setTipByPct((this.getTargetTipPct() + foodPlace.getTipPercentage())/2);
        foodPlace.distributeIncomeAndSalesTax(bill);

    }
}
