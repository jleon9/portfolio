package com.company;

import java.util.ArrayList;
import java.util.List;

public class Restaurant extends FoodPlace {

    private Staff cook;
    private Server server;

    public Restaurant(String name, double fixedCosts, Owner owner, Staff cook, Server server) {
        super(name, fixedCosts, owner);
        this.cook = cook;
        this.server = server;

    }

    public Staff getCook() {
        return cook;
    }

    public Server getServer() {
        return server;
    }

    @Override
    public String toString() {
        return "Name of restaurant: " + this.getName() +
                "\n" + "Owner: " + this.getOwner() +
                "\n" + "Cook: " + cook +
                "\n" + "Server: " + server;
    }

    @Override
    public void workShift(int hours) {
        double cook_add_income = this.cook.getSalaryPerHour()*hours;
        this.cook.income += cook_add_income;

        double server_add_income = this.server.getSalaryPerHour()*hours;
        this.server.income += server_add_income;

        Owner restaurantOwner = this.getOwner();
        double Owner_Expenses = restaurantOwner.getSalaryExpenses();
        restaurantOwner.setSalaryExpenses(Owner_Expenses + this.cook.income + this.server.income);

    }

    @Override
    public List<IncomeTaxPayer> getIncomeTaxPayers() {
        List<IncomeTaxPayer> LTP = new ArrayList<IncomeTaxPayer>();
        LTP.add(this.getOwner());
        LTP.add(this.server);
        LTP.add(this.cook);

        return LTP;
    }

    @Override
    public void distributeIncomeAndSalesTax(Check check) {
        Owner restaurantOwner = this.getOwner();
        restaurantOwner.income += check.getMenuPrice();
        double restaurantTip = check.getTip();
        this.cook.income += 0.2*restaurantTip;
        this.server.income += 0.8*restaurantTip;
        this.setTotalSalesTax(this.getTotalSalesTax() + check.getSalesTax());

    }

    @Override
    public double getTipPercentage() {
        return this.server.getTargetTipPct();
    }

}
