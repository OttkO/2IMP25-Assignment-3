package nl.tue.se.bridge;

import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.ling.Sentence;
import edu.stanford.nlp.parser.lexparser.LexicalizedParser;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.semgraph.SemanticGraph;
import edu.stanford.nlp.semgraph.SemanticGraphCoreAnnotations;
import edu.stanford.nlp.trees.*;
import edu.stanford.nlp.util.CoreMap;

import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.Properties;


/**
 * Created by Nathan on 3/17/2016.
 */
public class MainBridge {

    StanfordCoreNLP pipeline;

    public MainBridge() {
        Properties props = new Properties();
        props.setProperty("annotators", "tokenize, ssplit, pos, depparse");
        pipeline = new StanfordCoreNLP(props);
    }

    public List<List<String>> linesToDependencies(List<String> lines) {
        String text = ""; // Add your text here!

// create an empty Annotation just with the given text
        Annotation document = new Annotation(text);

// run all Annotators on this text
        pipeline.annotate(document);

        return null;
    }


    public List<String>lineToDependencies(String line) {


// create an empty Annotation just with the given text
        Annotation document = new Annotation(line);

// run all Annotators on this text
        pipeline.annotate(document);

        List<CoreMap> sentences = document.get(CoreAnnotations.SentencesAnnotation.class);

        SemanticGraph deps = null;

        for(CoreMap sentence: sentences) {
            // this is the Stanford dependency graph of the current sentence
             deps = sentence.get(SemanticGraphCoreAnnotations.CollapsedCCProcessedDependenciesAnnotation.class);
        }

        return depToStringArray(deps.typedDependencies());

    }

    private static List<String> depToStringArray(Collection<TypedDependency> deps) {
        List<String> out = new ArrayList<String>();

        for(TypedDependency dep : deps) {
            out.add(dep.toString());
        }

        return out;
    }

    public static void main(String[] args) {
        MainBridge bridge = new MainBridge();

        System.out.println(bridge.lineToDependencies("Some very long sentence, however, it is not that long!"));
    }
}
