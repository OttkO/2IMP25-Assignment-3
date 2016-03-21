package nl.tue.se.bridge;

import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.ling.Sentence;
import edu.stanford.nlp.parser.lexparser.LexicalizedParser;
import edu.stanford.nlp.trees.*;
import edu.stanford.nlp.util.CoreMap;

import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;


/**
 * Created by Nathan on 3/17/2016.
 */
public class MainBridge {

    private LexicalizedParser parser;
    private GrammaticalStructureFactory grammaticalStructureFactory;

    public MainBridge(int threads) {
        if(threads < 1) {
            throw new IllegalArgumentException("Zero threads is not possible, now is it?");
        }

        parser = LexicalizedParser.loadModel(
                "edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz",
                "-retainTmpSubcategories");
        TreebankLanguagePack tlp = new PennTreebankLanguagePack();

        grammaticalStructureFactory = tlp.grammaticalStructureFactory();
    }

    public List<List<String>> linesToDependencies(List<String> lines) {
        List<List<String>> out = new ArrayList<List<String>>();

        for(String line : lines) {
            out.add(lineToDependencies(line));
        }
        return out;
    }


    public List<String> lineToDependencies(String line) {

        String[] sent = line.split(" ");
        Tree parse = parser.apply(Sentence.toWordList(sent));
        GrammaticalStructure gs = grammaticalStructureFactory.newGrammaticalStructure(parse);
        return depToStringArray(gs.typedDependenciesCCprocessed());

    }

    private static List<String> depToStringArray(List<TypedDependency> deps) {
        List<String> out = new ArrayList<String>();

        for(TypedDependency dep : deps) {
            out.add(dep.toString());
        }

        return out;
    }

    public static void main(String[] args) {
        System.out.println("Hello");
    }
}
