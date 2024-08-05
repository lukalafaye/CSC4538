/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package itsudparis.application;

import org.apache.log4j.BasicConfigurator;
import org.apache.log4j.PropertyConfigurator;

import com.hp.hpl.jena.rdf.model.Model;
import itsudparis.tools.JenaEngine;

/**
 *
 * @author DO.ITSUDPARIS
 */
public class Main {
  
    /**
     * @param args rhe command line arguments
     */
   

public static void main(String[] args) {
	//on indique le chemin vers jena-log4j.properties (pour supprimer les warnings)
	String log4jConfPath = "/Users/amelbouzeghoub/Documents/Enseignement/ASR2020-2021/jena10/apache-jena-2.10.0/jena-log4j.properties";
	PropertyConfigurator.configure(log4jConfPath);
	//fin de la config log4j
	String NS = "";
	// lire le model a partir d'une ontologie
	Model model = JenaEngine.readModel("data/famille3.owl");
	if (model != null) {
	//lire le Namespace de l’ontologie
	NS = model.getNsPrefixURI("");
	
	// modifier le model
	// Ajouter une nouvelle femme dans le modele: Nora,50, estFilleDe Peter
	
	JenaEngine.createInstanceOfClass(model, NS, "Femme","Nora");
	JenaEngine.createInstanceOfClass(model, NS, "Personne","Nora");
	JenaEngine.updateValueOfDataTypeProperty(model, NS,"Nora", "age", 50);
	
	JenaEngine.updateValueOfObjectProperty(model, NS,"Nora", "estFilleDe", "Peter");
	//Ajouter un nouvel homme dans le modele: Rob, 51,seMarierAvec Nora
	JenaEngine.createInstanceOfClass(model, NS, "Homme","Rob");
	JenaEngine.updateValueOfDataTypeProperty(model, NS,"Rob", "age", 51);
	JenaEngine.updateValueOfDataTypeProperty(model, NS,"Rob", "nom", "Yeung");
//	JenaEngine.updateValueOfObjectProperty(model, NS,"Rob", "seMarierAvec", "Nora");
	//apply owl rules on the model
	Model owlInferencedModel =
	JenaEngine.readInferencedModelFromRuleFile(model, "data/owlrules.txt");
	// apply our rules on the owlInferencedModel
	Model inferedModel =
	JenaEngine.readInferencedModelFromRuleFile(owlInferencedModel,"data/rules.txt");
	// query on the model after inference
	System.out.println(JenaEngine.executeQueryFile(inferedModel,"data/query.txt"));
	} else {
	System.out.println("Error when reading model from ontology");
	}
	 
}
}

