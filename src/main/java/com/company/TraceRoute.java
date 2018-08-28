package com.company;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

class TraceRoute {

    private List<String> commands;

    TraceRoute() {
        commands = new ArrayList<>();
        commands.add("traceroute");
        commands.add("-w 1");
    }

    String getTracer(String ip) throws IOException {
        commands.add(ip);
        return doCommand(commands);
    }

    private String doCommand(List<String> command) throws IOException {
        String outputLine;
        StringBuilder outputTracer = new StringBuilder();


        ProcessBuilder pb = new ProcessBuilder(command);
        Process process = pb.start();

        BufferedReader stdInput = new BufferedReader(new InputStreamReader(process.getInputStream()));

        while ((outputLine = stdInput.readLine()) != null) {
            if (!outputLine.contains("!H") && outputLine.contains("ms")) {
                outputTracer.append(outputLine);
            }
        }
        return String.valueOf(outputTracer);
    }
}
