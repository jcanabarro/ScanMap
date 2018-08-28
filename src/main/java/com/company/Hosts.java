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

    private int getFinalSubIp( int position ) {
        return vectorIp.get(position) + (int) (Math.pow(2, (8 - Integer.bitCount(vectorMask.get(position)))) - 1);
    }

    List checkHosts() {
        int subIpStartI = vectorIp.get(2);
        int subIpFinishI = getFinalSubIp(2);

        int subIpStartJ = vectorIp.get(3);
        int subIpFinishJ = getFinalSubIp(3);

        for(int i = subIpStartI; i <= subIpFinishI; i++) {
            StringBuilder host = new StringBuilder();
            host.append(vectorIp.get(0)).append(".").append(vectorIp.get(1)).append(".").append(i);
            for (int j = subIpStartJ; j < subIpFinishJ; j++) {
                availableHosts.add(host + "." + j);
            }
        }
        return availableHosts;
    }
}

//https://stackoverflow.com/questions/3345857/how-to-get-a-list-of-ip-connected-in-same-network-subnet-using-java