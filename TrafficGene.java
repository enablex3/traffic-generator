import java.awt.*;       
import java.awt.event.*; 
import javax.swing.*; 
import java.io.*;
import java.util.*;

public class TrafficGene extends JFrame implements  ActionListener {

  JLabel lbltran;
  JLabel lblPort;
  JLabel lblSize;

  JComboBox tr;
  JComboBox ps;

  JTextField tfPort;
  JTextField tfSize;
  
  String selectedtr;
  String selectedps;
  JButton btnStart;

   public TrafficGene () {
     setLayout(new FlowLayout());
 
      setTitle("Traffic Generator");  
      setSize(700, 100);   
 

      lbltran = new JLabel("Transmission:");
      String[] TransType = {"TCP", "UDP"};
      tr = new JComboBox(TransType);
      //tr.setSelectedItem(0);
      selectedtr = (String)tr.getSelectedItem();
      add(lbltran);
      add(tr);


      lblPort = new JLabel("Port:");
      tfPort= new JTextField("",10); 
      add(lblPort);
      add(tfPort);

      lblSize = new JLabel("Packet Size:");
      String[] PacSize = {"B", "Kb","Mb", "Gb"};
      tfSize = new JTextField("",10); 
      ps = new JComboBox(PacSize);
      selectedps = (String)ps.getSelectedItem();
      add(lblSize);
      add(tfSize);
      add(ps);

      btnStart = new JButton("Start");   
      add(btnStart); 
      btnStart.addActionListener(this);

      // inspecting the container/components objects
      // System.out.println(this);
      // System.out.println(lblSize);
      // System.out.println(tfSize);
      // System.out.println(submit);
 
      setVisible(true);      
   }

   public static void main(String[] args)
   {
      new TrafficGene();
   }

   
   @Override
   public void actionPerformed(ActionEvent ev)
   {
      StringBuilder inputs = new StringBuilder();
      String info;
   //   BufferedReader stdInput = new BufferedReader(
   //         new InputStreamReader(info.getInputStream()));

   //   Writer file = new BufferedWriter(new OutputStreamWriter(
   //         new FileOutputStream("JsonFormat.txt"), "utf-8")); 

      String ttype = "";
      String prtnm = "";
      String psize = "";

   //try
         try 
         {
            ttype= "Transmission: " + selectedtr;
            prtnm= "Port: " + tfPort.getText();
            psize= "Packet Size: " + tfSize.getText()+ selectedps;

            inputs.append("{"+ ttype+ ", " + prtnm + ", "+ psize+"}");
            info = inputs.toString();

            File file = new File("inputs.txt");
            FileWriter fileWriter = new FileWriter(file);
            fileWriter.write(info);
            fileWriter.flush();
            fileWriter.close();

   //         while ((info = stdInput.readLine()) != null)
   //            { 
   //              System.out.println(info);  
   //              file.write(info+"\n");  
   //           }
   //         System.out.println(inputs);
   //         file.close(); 
         } 
         catch (Exception e) 
         {
              e.printStackTrace();
              System.exit(-1);
         }
   }

   
}