package org.pantsbuild.contrib.thrifty;

import org.pantsbuild.contrib.thrifty.common.ClientLog;
import org.pantsbuild.contrib.thrifty.common.Common;

public class ThriftyExample {
    public static void main(String [] args) {

        Common common = new Common.Builder()
                .timestamp(1L)
                .hostname("fake_hostname")
                .build();
        ClientLog clientLog = new ClientLog.Builder()
                .common(common)
                .message("fake_message")
                .build();
        System.out.println(clientLog);
    }
}
