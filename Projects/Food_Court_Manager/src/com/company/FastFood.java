package com.company;

import java.util.ArrayList;
import java.util.List;

public class FastFood extends FoodPlace {

    private List<Staff> staff = new ArrayList<>();

    public FastFood(String name, double fixedCosts, Owner owner, List<Staff> staff) {
        super(name, fixedCosts, owner);
        ArrayList<Staff> copy_staff = new ArrayList<Staff>();
        for (Staff s : staff) {
            copy_staff.add(s);
        }
        this.staff = copy_staff;
    }

    public List<Staff> getStaff() {
        return staff;
    }

    @Override
    public String toString() {
        StringBuilder builder = new StringBuilder();
        builder.append("Name of FastFood: " + this.getName() +
                "\n" + "Owner: " + this.getOwner());
        int index = 1;
        for (Staff staff: staff) {
            builder.append("\n" + "Staff " + index++ + " : " + staff );
        }
        return builder.toString();
    }

    @Override
    public void workShift(int hours) {
        Owner FFO = this.getOwner();
        double FFO_Expenses = 0;
        for (Staff s : staff) {
            double add_Expense = s.workHours(hours);
            FFO_Expenses += add_Expense;
        }
        FFO.setSalaryExpenses(FFO_Expenses);
    }

    @Override
    public List<IncomeTaxPayer> getIncomeTaxPayers() {
        ArrayList<IncomeTaxPayer> LTP = new ArrayList<IncomeTaxPayer>();
        LTP.add(this.getOwner());
        for (Staff s: staff) {
            LTP.add(s);
        }
        return LTP;
    }

    @Override
    public void distributeIncomeAndSalesTax(Check check) {
       /* ArrayList<IncomeTaxPayer> LTP = new ArrayList<IncomeTaxPayer>();
        LTP = (ArrayList<IncomeTaxPayer>) this.getIncomeTaxPayers();

        for (Object s : LTP) {
            if (s instanceof Owner) {
                ((IncomeTaxPayer) s).setIncome(((IncomeTaxPayer) s).getIncome() + check.getMenuPrice());
                LTP.remove(s);
            }
            else {
                ((IncomeTaxPayer) s).setIncome(((IncomeTaxPayer) s).getIncome() + check.getTip()/LTP.size());
            }
        } */

        Owner owner = this.getOwner();
        owner.setIncome( owner.getIncome() + check.getMenuPrice() );
        for (Staff staff: staff) {
            staff.setIncome( staff.getIncome() + check.getTip() / this.staff.size() );
        }
        this.setTotalSalesTax( this.getTotalSalesTax() + check.getSalesTax());


    }

    @Override
    public double getTipPercentage() {
        return 0;
    }
}