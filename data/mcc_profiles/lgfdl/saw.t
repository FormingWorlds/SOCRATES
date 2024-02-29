netcdf saw.t{                                                                   

dimensions:
    lat            =   1;
    lon            =   1;
    plev           = 122;


variables:
    float lat(lat);                                                           
             lat:units = "degree";                                            
             lat:title = "LATITUDE";                                         
    float lon(lon);                                                           
             lon:units = "degree";                                            
             lon:title = "LONGITUDE";                                        
    float plev(plev);                                                         
             plev:units = "Pa";                                               
             plev:title = "PRESSURE";                                        

    float t(plev,lon,lat);                                                     
             t:units = "K";                                                   
             t:title = "TEMPERATURE";                                                        

data:                                                                           
              lat =   .000000E+00;
              lon =   .000000E+00;
             plev =   .500000E-01,  .108300E+00,  .126260E+00,  .147210E+00,
                      .171640E+00,  .200110E+00,  .233320E+00,  .272030E+00,
                      .317160E+00,  .369780E+00,  .431130E+00,  .502660E+00,
                      .586060E+00,  .683300E+00,  .796670E+00,  .928850E+00,
                      .108300E+01,  .126260E+01,  .147210E+01,  .171640E+01,
                      .200110E+01,  .233320E+01,  .272030E+01,  .317160E+01,
                      .369780E+01,  .431130E+01,  .502660E+01,  .586060E+01,
                      .683300E+01,  .796670E+01,  .928850E+01,  .108300E+02,
                      .126260E+02,  .147210E+02,  .171640E+02,  .200110E+02,
                      .233320E+02,  .272030E+02,  .317160E+02,  .369780E+02,
                      .431130E+02,  .502660E+02,  .586060E+02,  .683300E+02,
                      .796670E+02,  .928850E+02,  .108300E+03,  .126260E+03,
                      .147210E+03,  .171640E+03,  .200110E+03,  .233320E+03,
                      .272030E+03,  .317160E+03,  .369780E+03,  .431130E+03,
                      .502660E+03,  .586060E+03,  .683300E+03,  .796670E+03,
                      .928850E+03,  .108300E+04,  .126260E+04,  .147210E+04,
                      .171640E+04,  .200110E+04,  .233320E+04,  .272030E+04,
                      .317160E+04,  .369780E+04,  .431130E+04,  .502660E+04,
                      .586060E+04,  .683300E+04,  .796670E+04,  .928850E+04,
                      .110000E+05,  .130000E+05,  .150000E+05,  .170000E+05,
                      .190000E+05,  .210000E+05,  .230000E+05,  .250000E+05,
                      .270000E+05,  .290000E+05,  .310000E+05,  .330000E+05,
                      .350000E+05,  .370000E+05,  .390000E+05,  .410000E+05,
                      .430000E+05,  .450000E+05,  .470000E+05,  .490000E+05,
                      .510000E+05,  .530000E+05,  .550000E+05,  .570000E+05,
                      .590000E+05,  .610000E+05,  .630000E+05,  .650000E+05,
                      .670000E+05,  .690000E+05,  .710000E+05,  .730000E+05,
                      .750000E+05,  .770000E+05,  .790000E+05,  .810000E+05,
                      .830000E+05,  .850000E+05,  .870000E+05,  .890000E+05,
                      .910000E+05,  .930000E+05,  .950000E+05,  .970000E+05,
                      .990000E+05,  .100650E+06;
                t =   .215400E+03,  .216300E+03,  .217510E+03,  .218720E+03,
                      .219930E+03,  .221160E+03,  .222390E+03,  .223620E+03,
                      .224870E+03,  .226120E+03,  .227370E+03,  .228630E+03,
                      .229900E+03,  .231180E+03,  .232460E+03,  .233750E+03,
                      .235040E+03,  .236350E+03,  .237650E+03,  .238970E+03,
                      .240290E+03,  .241620E+03,  .242950E+03,  .244270E+03,
                      .245470E+03,  .246470E+03,  .247320E+03,  .248120E+03,
                      .248920E+03,  .249720E+03,  .250520E+03,  .251330E+03,
                      .252130E+03,  .252940E+03,  .253750E+03,  .254570E+03,
                      .255380E+03,  .256200E+03,  .257020E+03,  .257840E+03,
                      .258560E+03,  .258750E+03,  .257600E+03,  .255220E+03,
                      .252400E+03,  .249550E+03,  .246720E+03,  .243930E+03,
                      .241170E+03,  .238440E+03,  .235740E+03,  .233080E+03,
                      .230440E+03,  .227850E+03,  .225360E+03,  .223180E+03,
                      .221490E+03,  .220150E+03,  .218930E+03,  .217750E+03,
                      .216620E+03,  .215570E+03,  .214570E+03,  .213610E+03,
                      .212730E+03,  .212120E+03,  .212030E+03,  .212390E+03,
                      .212920E+03,  .213490E+03,  .214070E+03,  .214650E+03,
                      .215240E+03,  .215820E+03,  .216400E+03,  .216850E+03,
                      .217050E+03,  .217070E+03,  .217070E+03,  .217070E+03,
                      .217070E+03,  .217070E+03,  .217070E+03,  .217070E+03,
                      .217130E+03,  .217680E+03,  .219280E+03,  .221680E+03,
                      .224190E+03,  .226620E+03,  .228940E+03,  .231170E+03,
                      .233310E+03,  .235360E+03,  .237320E+03,  .239210E+03,
                      .241010E+03,  .242730E+03,  .244360E+03,  .245900E+03,
                      .247350E+03,  .248700E+03,  .249960E+03,  .251120E+03,
                      .252200E+03,  .253200E+03,  .254120E+03,  .254980E+03,
                      .255780E+03,  .256520E+03,  .257220E+03,  .257850E+03,
                      .258410E+03,  .258830E+03,  .259070E+03,  .259100E+03,
                      .258930E+03,  .258620E+03,  .258230E+03,  .257810E+03,
                      .257420E+03,  .257170E+03;

}                                                                               
