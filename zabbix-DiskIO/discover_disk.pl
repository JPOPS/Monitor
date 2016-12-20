#!/usr/bin/perl

sub get_vmname_by_id
  {
  $vmname=`cat /etc/qemu-server/$_[0].conf | grep name | cut -d \: -f 2`;
  $vmname =~ s/^\s+//; #remove leading spaces
  $vmname =~ s/\s+$//; #remove trailing spaces
  return $vmname
  }

$first = 1;
print "{\n";
print "\t\"data\":[\n\n";

for (`cat /proc/diskstats`)
  {
  ($major,$minor,$disk) = m/^\s*([0-9]+)\s+([0-9]+)\s+(\S+)\s.*$/;
  $dmnamefile = "/sys/dev/block/$major:$minor/dm/name";
  $vmid= "";
  $vmname = "";
  $dmname = $disk;
  $diskdev = "/dev/$disk";
  # DM name
  if (-e $dmnamefile) {
    $dmname = `cat $dmnamefile`;
    $dmname =~ s/\n$//; #remove trailing \n
    $diskdev = "/dev/mapper/$dmname";
    # VM name and ID
    if ($dmname =~ m/^.*--([0-9]+)--.*$/) {
      $vmid = $1;
      #$vmname = get_vmname_by_id($vmid);
      }
    }
  #print("$major $minor $disk $diskdev $dmname $vmid $vmname \n");

  print "\t,\n" if not $first;
  $first = 0;

  print "\t{\n";
  print "\t\t\"{#DISK}\":\"$disk\",\n";
  print "\t\t\"{#DISKDEV}\":\"$diskdev\",\n";
  print "\t\t\"{#DMNAME}\":\"$dmname\",\n";
  print "\t\t\"{#VMNAME}\":\"$vmname\",\n";
  print "\t\t\"{#VMID}\":\"$vmid\"\n";
  print "\t}\n";
  }

print "\n\t]\n";
print "}\n";


