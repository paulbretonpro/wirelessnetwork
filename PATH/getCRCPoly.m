function gx = getCRCPoly(sizeCRC)
gx = zeros(1,1+sizeCRC);
gx(1) = 1;
switch sizeCRC
    case 8
        gx(1+[1 2 8]) = 1;
    case 16
        gx(1+[2 15 16]) = 1;
    case 24
        gx(1+[1 3 6 7 8 10 11 13 14 16 18 19 20 22 24]) = 1;
    case 32
        gx(1+[1 2 4 5 7 8 10 11 12 16 22 23 26 32]) = 1;
    otherwise
        error('imr:crc','unknwon CRC size');
end
end
