function  hardBits =QAM16_demod(qamVect)
%% 16-QAM hard demapper
% --- Gray encoding
%  -3     -1     1     3
%  10     11    01    00
% --- Voronoi region definition
bounds	= [-2 0 2]/(sqrt(2/3*15));
hardBits = zeros(1,4*length(qamVect));
%bounds	= (-sqrt(2)/2 0 sqrt(2)/2);
% --- Iterative hard demapping
for n = 1 : 1 : length(qamVect)
    % --- Decision for real part
    % Getting only real part
    realI	= real(qamVect(n));
    % Getting area of interest: from area 1 to 4
    decI	= 1+ (realI > bounds(1)) + (realI>bounds(2)) + (realI>bounds(3));
    % Convert into binary sequence based on Gray encoding scheme.
    if decI == 1
        hardBits(4*(n-1)+1) = 1;
        hardBits(4*(n-1)+3) = 0;
    elseif decI == 2
        hardBits(4*(n-1)+1) = 1;
        hardBits(4*(n-1)+3) = 1;
    elseif decI == 3
        hardBits(4*(n-1)+1) = 0;
        hardBits(4*(n-1)+3) = 1;
    elseif decI == 4
        hardBits(4*(n-1)+1) = 0;
        hardBits(4*(n-1)+3) = 0;
    end
    % --- Decision for imag part
    % Getting only imag part
    imagP	= imag(qamVect(n));
    % Getting area of interest: from area 1 to 4
    decQ	= 1+ (imagP > bounds(1)) + (imagP>bounds(2)) + (imagP>bounds(3));
    % Convert into binary sequence based on Gray encoding scheme.
    if decQ == 1
        hardBits(4*(n-1)+2) = 1;
        hardBits(4*(n-1)+4) = 0;
    elseif decQ == 2
        hardBits(4*(n-1)+2) = 1;
        hardBits(4*(n-1)+4) = 1;
    elseif decQ == 3
        hardBits(4*(n-1)+2) = 0;
        hardBits(4*(n-1)+4) = 1;
    elseif decQ == 4
        hardBits(4*(n-1)+2) = 0;
        hardBits(4*(n-1)+4) = 0;
    end
    r = 12;
    
end
