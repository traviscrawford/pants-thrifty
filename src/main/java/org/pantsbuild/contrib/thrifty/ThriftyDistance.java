package org.pantsbuild.contrib.thrifty;

import org.pantsbuild.example.distance.thriftjava.Distance;

public class ThriftyDistance {
    public static void main(String [] args) {
        Distance distance = new Distance.Builder()
                .Number(42L)
                .Unit("parsecs")
                .build();
        System.out.println(distance);
    }
}
