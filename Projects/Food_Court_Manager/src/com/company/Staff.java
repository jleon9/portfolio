package com.company;

public class Staff extends IncomeTaxPayer {

    private int salaryPerHour;
    final private int incomeTaxPercentage = 25;

    public Staff(String name, boolean isCook) {
        super(name);
        if (isCook == true) {
            this.salaryPerHour = 20;
        }
        else {
            this.salaryPerHour = 10;
        }
    }

    public int getSalaryPerHour() {
        return salaryPerHour;
    }

    public int getIncomeTaxPercentage() {
        return incomeTaxPercentage;
    }

    public double workHours(int numHours) {
        double addIncome = numHours*this.getSalaryPerHour();
        this.setIncome(this.getIncome() + numHours*this.getSalaryPerHour());
        return addIncome;
    }

    @Override
    public double calculateIncomeTax() {
        double incomeTax = (this.getIncomeTaxPercentage()/100.00)*this.getIncome();
        return incomeTax;
    }

}