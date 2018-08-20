package com.company;

import org.apache.commons.net.util.SubnetUtils;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

class Hosts {

    private int timeout;
    private String ip;
    private String networkIp;
    private ArrayList<Integer> vectorMask;
    private ArrayList<Integer> vectorIp;
    private int shotMask;
    private List availableHosts;
    private SubnetUtils utils;

    Hosts (int timeout, String ip, String mask) {
        this.vectorMask = new ArrayList<>();
        this.vectorIp = new ArrayList<>();
        this.timeout = timeout;
        availableHosts = new ArrayList();
        this.ip = ip;
        String[] mask1 = mask.split("\\.");
        String[] ip1 = ip.split("\\.");

        for (String submask : mask1){
            int subString = Integer.valueOf(submask);
            vectorMask.add(subString);
            shotMask += Integer.bitCount(subString);
        }
        utils = new SubnetUtils(this.ip + "/" + this.shotMask);

        for (String subip : ip1){
            int subString = Integer.valueOf(subip);
            vectorIp.add(subString);
        }
    }

    private boolean getAvailableHost(StringBuilder address) {
        return utils.getInfo().isInRange(String.valueOf(address));
    }

    List checkHosts() throws IOException {
        int subIpStart = vectorIp.get(2);
        int countZeroSubIp = (int) (Math.pow(2, (8 - Integer.bitCount(vectorMask.get(2)))) - 1);
        int subIpFinish = vectorIp.get(2) + countZeroSubIp;
        for(int i = subIpStart; i < subIpFinish; i++) {
            StringBuilder host = new StringBuilder();
            host.append(vectorIp.get(0)).append(".").append(vectorIp.get(1)).append(".").append(i);
            for (int j = 1; j < 255; j++) {
                StringBuilder address = new StringBuilder(host);
                address.append(".").append(j);
                if (getAvailableHost(address)) {
                    availableHosts.add(address.toString());
                }
            }
        }
        return availableHosts;
    }
}


//https://stackoverflow.com/questions/3345857/how-to-get-a-list-of-ip-connected-in-same-network-subnet-using-java