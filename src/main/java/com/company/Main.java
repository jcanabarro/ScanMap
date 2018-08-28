package com.company;

import java.io.IOException;
import java.util.List;

public class Main {

    public static void main(String[] args) throws IOException {

        Hosts host = new Hosts(100, "10.81.80.0", "255.255.255.0");

        List listhost = host.checkHosts();

        for (Object hosts:listhost) {
            TraceRoute tr = new TraceRoute();
            String actualTrace = tr.getTracer(String.valueOf(hosts));
            if(actualTrace != null && !actualTrace.isEmpty()) {
                System.out.println(actualTrace);
            }
        }
    }
}
