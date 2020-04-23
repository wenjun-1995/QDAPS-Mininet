#include <core.p4>
#include <v1model.p4>

header ethernet_t {
    bit<48> dstAddr;
    bit<48> srcAddr;
    bit<16> etherType;
}

header ipv4_t {
    bit<4>  version;
    bit<4>  ihl;
    bit<8>  diffserv;
    bit<16> totalLen;
    bit<16> identification;
    bit<3>  flags;
    bit<13> fragOffset;
    bit<8>  ttl;
    bit<8>  protocol;
    bit<16> hdrChecksum;
    bit<32> srcAddr;
    bit<32> dstAddr;
}

header tcp_t {
    bit<16> srcPort;
    bit<16> dstPort;
    bit<32> seqNo;
    bit<32> ackNo;
    bit<4>  dataOffset;
    bit<3>  res;
    bit<3>  ecn;
    bit<6>  ctrl;
    bit<16> window;
    bit<16> checksum;
    bit<16> urgentPtr;
}

struct intrinsic_metadata_t {
    bit<48> ingress_global_timestamp;
}

struct ingress_metadata_t {
    bit<32> packet_id;  
    bit<32> packet_map_index;
}
	
struct queueing_metadata_t {
    bit<19> deq_qdepth_0;      
    bit<19> deq_qdepth_1;
    bit<19> deq_qdepth_2;
    bit<19> deq_qdepth_3;
    bit<19> deq_qdepth_4;      
    bit<19> deq_qdepth_5;
    bit<19> deq_qdepth_6;
    bit<19> deq_qdepth_7;
}

struct metadata {
 intrinsic_metadata_t intrinsic_metadata;
 queueing_metadata_t  queueing_metadata;
 standard_metadata_t  standard_metadata;
 ingress_metadata_t   ingress_metadata;
}

struct headers {
    @name(".ethernet") 
    ethernet_t ethernet;
    @name(".ipv4") 
    ipv4_t     ipv4;
    @name(".tcp") 
    tcp_t      tcp;
}

parser ParserImpl(packet_in packet, out headers hdr, inout metadata meta, inout standard_metadata_t standard_metadata) {
    @name(".parse_ethernet") state parse_ethernet {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType) {
            16w0x800: parse_ipv4;
            default: accept;
        }
    }
    @name(".parse_ipv4") state parse_ipv4 {
        packet.extract(hdr.ipv4);
        transition select(hdr.ipv4.protocol) {
            8w6: parse_tcp;
            default: accept;
        }
    }
    @name(".parse_tcp") state parse_tcp {
        packet.extract(hdr.tcp);
        transition accept;
    }
    @name(".start") state start {
        transition parse_ethernet;
    }
}

control egress(inout headers hdr, inout metadata meta, inout standard_metadata_t standard_metadata) {
    apply {
    
   }
}
    
control ingress(inout headers hdr, inout metadata meta, inout standard_metadata_t standard_metadata) {

    register<bit<48>>(1)  qlength_1_reg;  //Store the queuing time of four queues
    register<bit<48>>(1)  qlength_2_reg;
    register<bit<48>>(1)  qlength_3_reg;
    register<bit<48>>(1)  qlength_4_reg;

    register<bit<48>>(8192) wait_time_reg;
    //register<bit<32>>(8192) packet_id_reg;  //Store packet id
    register<bit<48>>(8192)  packet_lasttime; //The arrival time of last packet 
    register<bit<9>>(8192)   port_reg;

    @name(".set_nhop") action set_nhop(bit<9> port) {
        standard_metadata.egress_spec = port;
        hdr.ipv4.ttl = hdr.ipv4.ttl - 1;
    }


    @name(".get_packet_id") action get_packet_id() {  
      hash(meta.ingress_metadata.packet_map_index, HashAlgorithm.crc16, (bit<13>)0, { hdr.ipv4.srcAddr, hdr.ipv4.dstAddr, hdr.ipv4.protocol, hdr.tcp.srcPort, hdr.tcp.dstPort }, (bit<26>)8192);   
   }

    @name(".set_nhop_random3") action set_nhop_random3() {  

      
      bit<48> qdepth1;
      qlength_1_reg.read(qdepth1,0);
      bit<48> qdepth2;
      qlength_2_reg.read(qdepth2,0);
      bit<48> qdepth3;
      qlength_3_reg.read(qdepth3,0);
      bit<48> qdepth4;
      qlength_4_reg.read(qdepth4,0);

      
      bit<48> wait_time;
      wait_time_reg.read(wait_time,meta.ingress_metadata.packet_map_index); //How long will it take for the last packet to leave the queue

      bit<9> port=0;

      bit<48> last_time; 
      packet_lasttime.read(last_time,meta.ingress_metadata.packet_map_index);

      bit<48> time_gap;
      time_gap = meta.intrinsic_metadata.ingress_global_timestamp - last_time; 

      qdepth1=qdepth1-time_gap; //dequeue
      if(qdepth1 < 0) {
	       qdepth1=0;
	  }

      qdepth2=qdepth2-time_gap;
      if (qdepth2 < 0) {
		qdepth2=0;
	  }

      qdepth3=qdepth3-time_gap;
      if (qdepth3 < 0) {
	     qdepth3=0;
	  }

      qdepth4=qdepth4-time_gap;
       if (qdepth4 < 0) {
	     qdepth4=0;
	  }
     
      bit<48> left_time; 
      left_time = wait_time - time_gap;

      
      bit<48> tem;
      bit<32> mark = 0;
      bit<48> wait_time_x = 0; 
      bit<9> port_temp = 0;
      bit<48> a;
      bit<48> b;
      bit<48> c;
      bit<48> d;

      a = qdepth1;
      b = qdepth2;
      c = qdepth3;
      d = qdepth4;
 
      if(a>b)
      {tem=a;a=b;b=tem;}
      if(a>c)
      {tem=a;a=c;c=tem;}
      if(a>d)
      {tem=a;a=d;d=tem;} 
      if(b>c)
      {tem=b;b=c;c=tem;}
      if(b>d)
      {tem=b;b=d;d=tem;}
      if(c>d)
      {tem=c;c=d;d=tem;}

      if (a == qdepth1)
           {
              port_temp = 5;
           }
      if (a == qdepth2)
           {
              port_temp = 6;
           }
      if (a == qdepth3)
           {
              port_temp = 7;
           }
      if (a == qdepth4)
           {
              port_temp = 8;
           }
     
      if (mark == 0)
           {
              if (a>=left_time)
                 { mark = 1; wait_time_x = a;} 
           }
      if (mark == 0)
           {
              if (b>=left_time)
                 { mark = 1; wait_time_x = b;}
           }
      if (mark == 0)
           {
              if (c>=left_time)
                 { mark = 1; wait_time_x = c;}
           }
      if (mark == 0)
           {
              if (d>=left_time)
                 { mark = 1; wait_time_x = d;}
           }

      port_reg.read(port,(bit<32>)meta.ingress_metadata.packet_map_index);  

      //The bandwidth is set as 20Mbps, it takes 600 microseconds to handle a packet.
      if (mark == 0)  
           {

                if (port == 5 && qdepth1 <= 24600) //24600 = 41 * 600
                 {
                    qdepth1 = qdepth1+600; 
                    wait_time_x=qdepth1;
                 }
                 if (port == 6 && qdepth2 <= 24600)
                 {
                    qdepth2 = qdepth2+600;
                    wait_time_x=qdepth2;
                 }
                 if (port == 7 && qdepth3 <= 24600)
                 {
                    qdepth3 = qdepth3+600;
                    wait_time_x=qdepth3;
                 }
                 if (port == 8 && qdepth4 <= 24600)
                 {
                    qdepth4 = qdepth4+600;
                    wait_time_x=qdepth4;
                 }

                
                if (port_temp == 5)  //select the shortest queue
                 {
                    qdepth1 = qdepth1+600; 
                    wait_time_x=qdepth1;
                    port = 5;
                 }
                if (port_temp == 6)
                 {
                    qdepth2 = qdepth2+600; 
                    wait_time_x=qdepth2;
                    port = 6;
                 }
                if (port_temp == 7)
                 {
                    qdepth3 = qdepth3+600; 
                    wait_time_x=qdepth3;
                    port = 7;
                 }
                if (port_temp == 8)
                 {
                    qdepth4 = qdepth4+600; 
                    wait_time_x=qdepth4;
                    port = 8;
                 }
          }
       
     
      if (mark == 1)
          {
            if (wait_time_x == qdepth1)
              { port = 5; qdepth1=qdepth1+600;wait_time_x=qdepth1;}
            if (wait_time_x == qdepth2)
              { port = 6; qdepth2=qdepth2+600;wait_time_x=qdepth2;}
            if (wait_time_x == qdepth3)
              { port = 7; qdepth3=qdepth3+600;wait_time_x=qdepth3;}
            if (wait_time_x == qdepth4)
              { port = 8; qdepth4=qdepth4+600;wait_time_x=qdepth4;}
          }

       qlength_1_reg.write(0,qdepth1);
       qlength_2_reg.write(0,qdepth2);
       qlength_3_reg.write(0,qdepth3);
       qlength_4_reg.write(0,qdepth4);

       packet_lasttime.write(meta.ingress_metadata.packet_map_index, (bit<48>)meta.intrinsic_metadata.ingress_global_timestamp);
       wait_time_reg.write(meta.ingress_metadata.packet_map_index,wait_time_x);
       port_reg.write(meta.ingress_metadata.packet_map_index,port);
       standard_metadata.egress_spec = port;
       hdr.ipv4.ttl = hdr.ipv4.ttl - 1;
    }
   
  
    @name(".get_id") table get_id {  
       actions = {
         get_packet_id;
     }
    }

    @name(".forward1") table forward1 {
        actions = {
            set_nhop;
        }
        key = {
            hdr.ipv4.dstAddr: exact;
        }
        size = 512;
    }
     

    @name(".forward4") table forward4 {  
        actions = {
            set_nhop_random3;
        }
        key = {
            hdr.ipv4.dstAddr: exact;
        }
        size = 512;
    }

    apply {
        if (hdr.ipv4.isValid() && hdr.ipv4.ttl > 8w0) {
           forward1.apply();
           get_id.apply();  
           forward4.apply();
    }
 }
}
control DeparserImpl(packet_out packet, in headers hdr) {
    apply {
        packet.emit(hdr.ethernet);
        packet.emit(hdr.ipv4);
        packet.emit(hdr.tcp);
    }
}

control verifyChecksum(inout headers hdr, inout metadata meta) {
    apply {
        verify_checksum(true, { hdr.ipv4.version, hdr.ipv4.ihl, hdr.ipv4.diffserv, hdr.ipv4.totalLen, hdr.ipv4.identification, hdr.ipv4.flags, hdr.ipv4.fragOffset, hdr.ipv4.ttl, hdr.ipv4.protocol, hdr.ipv4.srcAddr, hdr.ipv4.dstAddr }, hdr.ipv4.hdrChecksum, HashAlgorithm.csum16);
    }
}

control computeChecksum(inout headers hdr, inout metadata meta) {
    apply {
        update_checksum(true, { hdr.ipv4.version, hdr.ipv4.ihl, hdr.ipv4.diffserv, hdr.ipv4.totalLen, hdr.ipv4.identification, hdr.ipv4.flags, hdr.ipv4.fragOffset, hdr.ipv4.ttl, hdr.ipv4.protocol, hdr.ipv4.srcAddr, hdr.ipv4.dstAddr }, hdr.ipv4.hdrChecksum, HashAlgorithm.csum16);
    }
}

V1Switch(ParserImpl(), verifyChecksum(), ingress(), egress(), computeChecksum(), DeparserImpl()) main;

