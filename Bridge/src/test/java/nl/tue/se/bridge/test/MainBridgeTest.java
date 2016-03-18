package nl.tue.se.bridge.test;

import nl.tue.se.bridge.MainBridge;
import org.json.JSONArray;
import org.junit.BeforeClass;
import org.junit.Test;

import java.util.List;

/**
 * Created by Nathan on 3/17/2016.
 */
public class MainBridgeTest {

    private static MainBridge bridge;

    @BeforeClass
    public static void setUp() {
        bridge = new MainBridge();
    }

    @Test
    public void simpleTest() {
        List<String> deps = bridge.lineToDependencies("What are you trying to do?");
        printRoughJson(deps);
    }

    @Test
    public void refTest() {
        List<String> deps = bridge.lineToDependencies("Why can't you just store the 'Range'?");
        printRoughJson(deps);
    }

    private void printRoughJson(List<String> deps) {
        JSONArray arr = new JSONArray(deps);

        System.out.println(arr.toString());
    }
}
