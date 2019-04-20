import java.awt.*;       
import java.awt.event.*; 
import javax.swing.*; 
import java.io.*;
import java.util.*;
import java.lang.*;

public class TrafficGene extends JFrame implements ActionListener {

  JPanel p = new JPanel();
  JPanel pnl = new JPanel();
  JPanel pl = new JPanel();
  JPanel pn = new JPanel();
  JPanel sp = new JPanel();

  JLabel lbltran;
  JLabel lblPort = new JLabel("Port(s):");
  JLabel lblSize;
  JLabel lblTrgt;
  JLabel lblDOS = new JLabel("DOS:");
  JLabel lblhost;

  JComboBox tr;
  JComboBox bs;
  JComboBox dos;
  JComboBox lh;

  JTextField tfPort1 = new JTextField("",6); 
  JTextField tfPort2 = new JTextField("",6);
  JTextField tfPort3 = new JTextField("",6);
  JTextField tfPort4 = new JTextField("",6);
  JTextField tfPort5 = new JTextField("",6); 

  JTextField tfSize;

  JTextField tfTrgt1;
  JTextField tfTrgt2;
  JTextField tfTrgt3;
  JTextField tfTrgt4;
  JTextField tfTrgt5;

  JTextArea sout = new JTextArea(20, 50);
  JScrollPane scrollPane;
  String selectedtr;
  String selectedbs;
  String selectedos;
  String[] tempsArray;
  String bots[][]=new String[10][4];
  String lch;

  ButtonGroup group = new ButtonGroup();

  JButton btnStart;
  JButton btnGO = new JButton("GO");  
  JButton btnStop = new JButton("Stop");  
  JButton btnARP = new JButton("ARP Scan");  

   public TrafficGene () {
      setLayout(new FlowLayout());
      setTitle("Traffic Generator");
      setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);  
      setSize(720, 620);   

      lbltran = new JLabel("Transmission:");
      String[] TransType = {"TCP", "UDP", "ICMP"};
      tr = new JComboBox(TransType);
      tr.setSelectedItem(0);
      selectedtr = (String)tr.getSelectedItem();
      tr.addActionListener(this);
      pl.setLayout(new GridLayout(9,1));
      add(pl);
      pl.add(lbltran);
      pl.add(tr);

      lblSize = new JLabel("Buffer Size:");
      String[] BufSize = {"B", "KB"};
      tfSize = new JTextField("",10); 
      bs = new JComboBox(BufSize);
      selectedbs = (String)bs.getSelectedItem();
      bs.addActionListener(this);
      pl.add(lblSize);
      pl.add(tfSize);
      pl.add(bs);

      p.setLayout(new GridLayout(9,1));
      add(p);
      p.add(lblPort);
      p.add(tfPort1);
      p.add(tfPort2);
      p.add(tfPort3);
      p.add(tfPort4);
      p.add(tfPort5);

      lblTrgt = new JLabel("Target(s):");
      tfTrgt1= new JTextField("",10); 
      tfTrgt2= new JTextField("",10); 
      tfTrgt3= new JTextField("",10);  
      tfTrgt4= new JTextField("",10); 
      tfTrgt5= new JTextField("",10); 
      pnl.setLayout(new GridLayout(9,1));
      add(pnl);
      pnl.add(lblTrgt);
      pnl.add(tfTrgt1);
      pnl.add(tfTrgt2);
      pnl.add(tfTrgt3);
      pnl.add(tfTrgt4);
      pnl.add(tfTrgt5);

      String[] DOS = {"NONE", "SINGLE", "DISTRIBUTED"};
      dos = new JComboBox(DOS);
      dos.setSelectedItem(0);
      selectedos = (String)dos.getSelectedItem();
      dos.addActionListener(this);
      p.add(lblDOS);
      p.add(dos);

      lblhost = new JLabel("Include LocalHost?:");
      String[] lhost = {"No", "Yes"};
      lh = new JComboBox(lhost);
      lch = (String)lh.getSelectedItem();
      pnl.add(lblhost);
      pnl.add(lh);
      lh.setEnabled(false);

      pn.setLayout(new GridLayout(1,4));
      add(pn);
      btnStart = new JButton("Start");  
      pn.add(btnStart); 
      btnStart.addActionListener(this);
      pn.add(btnGO);   
      btnGO.addActionListener(this);   
      pn.add(btnStop); 
      btnStop.setEnabled(false);  
      pn.add(btnARP); 
      btnARP.addActionListener(this);

      sout.setForeground(Color.blue);
      scrollPane = new JScrollPane(sout, JScrollPane.VERTICAL_SCROLLBAR_ALWAYS, JScrollPane.HORIZONTAL_SCROLLBAR_ALWAYS);
      add(sp); 
      sp.add(scrollPane);
      sout.setText("Stdout:");
      sout.setLineWrap(true);
      sout.setEditable(false); 

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
      StringBuilder pm= new StringBuilder();
      String[] g= new String[5];
      String ttype = "";
      String prtnm = "";
      String bsize = "";
      String trgts = "";
      String dos_ = "";
      StringBuilder bot= new StringBuilder();
      String lc="";
      if (ev.getSource() == tr)
      {
      //   JComboBox cb = (JComboBox) ev.getSource();
      //   String type = (String)cb.getSelectedItem();
         selectedtr = (String)tr.getSelectedItem();
         switch (selectedtr)
         {
            case "UDP":
            selectedtr = "UDP";
               break;
            case "ICMP":
            selectedtr = "ICMP";
               break;
            default: selectedtr = "TCP";
               break;
         }
      }

      if (ev.getSource() == lh)
      {
       lch = (String)lh.getSelectedItem();
       switch (lch)
         {
          case "Yes":
          lch = "Yes";
             break;
          default: lch = "No";
             break;                     
         }
      }

      if (ev.getSource() == bs)
      {
         selectedbs = (String)bs.getSelectedItem();
         switch (selectedbs)
         {
            case "KB":
            selectedbs = "KB";
               break;
            default: selectedbs = "B";
               break;                     
         }
      }

      if (ev.getSource() == dos)
      {
         selectedos = (String)dos.getSelectedItem();
         switch (selectedos)
         {
            case "SINGLE":
            selectedos = "SINGLE";
            btnStop.setEnabled(true);   
            btnStop.addActionListener(this);       
               break;
            case "DISTRIBUTED":
            selectedos = "DISTRIBUTED";
            btnStop.setEnabled(true);   
            btnStop.addActionListener(this);
            lh.setEnabled(true);
            lh.addActionListener(this);

         try
         {   
            String token = "";
            BufferedReader f1 = new BufferedReader(new FileReader("botnet.txt"));
            Scanner scanner=new Scanner(f1);
            scanner.useDelimiter(",\\s*|\\r\\n");
            ArrayList<String> temps = new ArrayList<String>();
            while (scanner.hasNext())
             {
              token = scanner.next();
              temps.add(token);
             }
            scanner.close();
             tempsArray = temps.toArray(new String[0]);
         } 
            //for (String tst : tempsArray)
            //{System.out.println(tst);}
         catch (FileNotFoundException e)
          {
             System.out.println("Error -- FileNotFoundException");
          }
               break;
            default: selectedos = "NONE";
            btnStop.setEnabled(false);      
               break;                     
         }
      }

      if (ev.getSource()== btnGO)
        {
          try
            { 
              btnStop.setEnabled(true);   
              InputStream stderr = null;
              InputStream stdout = null;
///****************************THE WHOLE PATH IS NEEDED********************************
///********************************///********************************
              String command = "python C:\\Users\\User\\Desktop\\traffic-generator\\TrafficGenerator.py"; ////
              Runtime r  = Runtime.getRuntime(); 
              Process proc = r.exec(command);
              stderr = proc.getErrorStream ();
              stdout = proc.getInputStream ();
              int k;
               while((k = stderr.read()) != -1)
               {
         	     char e = (char)k;
         	     System.out.print(e);
         	     sout.append(String.valueOf(e));
               }
             int i;
              while ((i = stdout.read()) != -1 )
               { 
                 char c = (char)i;
                 System.out.print(c);
                 sout.append(String.valueOf(c));
               }
           }
          catch (IOException e) 
           { 
           e.printStackTrace(); 
           }
        }

      if (ev.getSource()== btnStop)
        {
          try
           {
        	    InputStream stderr = null;
        	    InputStream stdout = null;
        	    String command = "python C:\\Users\\User\\Desktop\\traffic-generator\\TerminateDDOS.py";
        	    Runtime r = Runtime.getRuntime();
        	    Process proc = r.exec(command);
        	    stderr = proc.getErrorStream();
        	    stdout = proc.getInputStream();
             int k;
              while((k = stderr.read()) != -1)
                {
           	     char e = (char)k;
           	     System.out.print(e);
           	     sout.append(String.valueOf(e));
                }
        	    int i;
        	     while ((i = stdout.read()) != -1)
        	       {
        	    	  char c = (char)i;
        	    	  System.out.print(c);
        	    	  sout.append(String.valueOf(c));
        	       }
          }
          catch (IOException e)
           {
        	    e.printStackTrace();
           }
        }

      if (ev.getSource()== btnARP)
        {
          try
           {
             InputStream stderr = null;
             InputStream stdout = null;
             String command = "python C:\\Users\\User\\Desktop\\traffic-generator\\arp.py";
             Runtime r = Runtime.getRuntime();
             Process proc = r.exec(command);
             stderr = proc.getErrorStream();
             stdout = proc.getInputStream();
             int k;
              while((k = stderr.read()) != -1)
              {
                 char e = (char)k;
                 System.out.print(e);
                 sout.append(String.valueOf(e));
              }
             int i;
              while ((i = stdout.read()) != -1)
                {
                  char c = (char)i;
                  System.out.print(c);
                  sout.append(String.valueOf(c));
                }
          }
          catch (IOException e)
            {
             e.printStackTrace();
            }  
        }

      if (ev.getSource()== btnStart)
        {
         if ( (selectedbs == "KB" && Integer.parseInt(tfSize.getText()) > 64) || (selectedbs == "B" && Integer.parseInt(tfSize.getText()) > 64000) || Integer.parseInt(tfSize.getText()) <= 0)
          JOptionPane.showMessageDialog (null, "More than 64 is not allowed", "Error", JOptionPane.ERROR_MESSAGE);

         else
         {
          try 
          {

            /* { Target(s):  [192.168.120.21, 192.168.120.50], 
                 Port(s):  [21, 22],
                 Transmission:  UDP, 
                 BufferSize: 50KB, 
                 DOS: Distributed, 
                 Bots: {192.168.120.44: [root, toor], 192.168.120.100: [user_100, mypass]},
                 Localhost?: Yes }  */

            ttype = "\"Transmission\": " + "\"" + selectedtr + "\"";
           // for(int i =0; i <=5; i++) {}
            pm.append(tfPort1.getText());
            pm.append(", "+ tfPort2.getText());
            pm.append(", "+ tfPort3.getText());
            pm.append(", "+ tfPort4.getText());
            pm.append(", "+ tfPort5.getText());
         // prtnm = "\"Port(s)\": " + Arrays.toString(pm);
            prtnm = "\"Port(s)\": " +"\""+"[" +pm.toString() + "]"+"\"";

            bsize = "\"Packet Size\": " + "\""+ tfSize.getText()+ selectedbs+"\"";

            g[0] = tfTrgt1.getText();
            g[1] = tfTrgt2.getText();
            g[2] = tfTrgt3.getText();
            g[3] = tfTrgt4.getText();
            g[4] = tfTrgt5.getText();
            trgts = "\"Targets(s)\": " + "\""+ Arrays.toString(g)+ "\"";

            dos_ = "\"DOS\": " + "\"" + selectedos + "\"";

            //BOTS///////
            if (selectedos == "DISTRIBUTED")
            {
            int count=0;
            bot.append("\""+ "Bots" + "\": {");
            for(int i=0;i<10;i++)
            {
              for(int j=0;j<4;j++)
               {
                if(count==tempsArray.length) break;
                bots[i][j]=tempsArray[count];
               // System.out.printf("bots[%d][%d]= %s\n",i,j,bots[i][j]);

                if (j==0)
                 {
                  bots[i][j]="\""+ bots[i][j] + "\": ";
                  bot.append(bots[i][j]);
                 }
                if (j==1)
                 {
                  bots[i][j]="[\""+ bots[i][j] + "\", ";
                  bot.append(bots[i][j]);
                 }
                if (j==2)
                 {
                  bots[i][j]="\""+ bots[i][j] + "\"], ";
                  bot.append(bots[i][j]);
                 }
                if (j==3)
                 {
                   bots[i][j]= bots[i][j] + ", ";
                   bot.append(bots[i][j]);
                 }
                count++;
               }
            }

            bot.append("}, ");
            //System.out.println(bot);
            //System.out.println("Count is "+count);
         }

            lc= "\"Localhost?\": " + "\"" + lch+ "\""; 

            inputs.append("{"+ ttype+ ", " + prtnm + ", " + bsize + ", "+ trgts + ", "+ dos_ +", "+ lc + "}");
            info = inputs.toString();

            File file = new File("inputs.txt");
            FileWriter fileWriter = new FileWriter(file);
           // BufferedWriter fileWriter= new BufferedWriter(new FileWriter(file, true));
            fileWriter.write(info);
            fileWriter.flush();
            fileWriter.close();
   
            System.out.println(inputs);
          } 

          catch (Exception e) 
          {
              e.printStackTrace();
              System.exit(-1);
          }

         JOptionPane.showMessageDialog (null, "Inputs are stored.\n * Please press 'GO' when ready.", "Saved!", JOptionPane.INFORMATION_MESSAGE);

         }
      }
   }
}
