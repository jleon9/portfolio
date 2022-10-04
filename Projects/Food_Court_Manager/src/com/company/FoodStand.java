package com.company;
import java.util.ArrayList;
import java.util.List;

public class FoodStand extends FoodPlace {

    public FoodStand(String name, double fixedCosts, WorkingOwner owner) {
        super(name, fixedCosts, owner);
    }

    @Override
    public String toString() {
        return "Name of FoodStand: " + this.getName() +
                "\n" + "Owner: " + this.getOwner();
    }

    @Override
    public void workShift(int hours) {
        // no salaried workers so do nothing
    }

    @Override
    public List<IncomeTaxPayer> getIncomeTaxPayers() {
        List<IncomeTaxPayer> LTP = new ArrayList<IncomeTaxPayer>();
        LTP.add(this.getOwner());

        return LTP;

    }

    @Override
    public void distributeIncomeAndSalesTax(Check check) {
        Owner foodStandOwner = this.getOwner();
        foodStandOwner.income += check.getMenuPrice();
        double foodStandTip = check.getTip();
        foodStandOwner.income += foodStandTip;
        this.setTotalSalesTax(this.getTotalSalesTax() + check.getSalesTax());

    }

    @Override
    public double getTipPercentage() {
        Owner foodStandOwner = this.getOwner();
        double FSO_TarTipPct = ((WorkingOwner) foodStandOwner).getTargetTipPct();
        return FSO_TarTipPct;
    }
}