package com.company;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

public class Ping {

    private List<String> commands;

    Ping() {
        commands = new ArrayList<>();
        commands.add("ping");
        commands.add("-c");
        commands.add("5");
    }

    public void getLatency (String ip) throws IOException {
        commands.add(ip);
        doCommand(commands);
    }

    private void doCommand(List<String> command) throws IOException {
        String s;

        ProcessBuilder pb = new ProcessBuilder(command);
        Process process = pb.start();

        BufferedReader stdInput = new BufferedReader(new InputStreamReader(process.getInputStream()));
        BufferedReader stdError = new BufferedReader(new InputStreamReader(process.getErrorStream()));

        System.out.println("Here is the standard output of the command:\n");
        while ((s = stdInput.readLine()) != null) {
            System.out.println(s);
        }

        System.out.println("Here is the standard error of the command (if any):\n");
        while ((s = stdError.readLine()) != null) {
            System.out.println(s);
        }
    }
}
