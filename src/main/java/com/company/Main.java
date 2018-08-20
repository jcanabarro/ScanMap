package com.company;

import java.io.IOException;
import java.util.List;

public class Main {

    public static void main(String[] args) throws IOException {
//        Ping pg = new Ping();
//        pg.getLatency("10.81.80.208");

        Hosts host = new Hosts(100, "10.81.80.0", "255.255.248.0");

        List listhost = host.checkHosts();

        for (Object hosts:listhost) {
            System.out.println(hosts);
        }
    }
}
