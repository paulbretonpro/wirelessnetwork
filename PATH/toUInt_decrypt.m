function out = toUInt_decrypt(userId,mess)
    cesarVect =   [5
                   6
                   10
                   23
                   18
                   3
                   9
                   14
                   2
                   13
                   8
                   17
                   0
                   12
                   4
                   22
                   11
                   7
                   20
                   25
                   15
                   19
                   24
                   21
                   1
                   16];
    id= cesarVect(mod(userId,26))
    out = cesarDecode(id,toUInt(mess));
end


% cesarDecode.m
%   Apply Cesar decosing with the use of the key 'key'
%  --- Syntax 
%       messDec = cesarDecode(key,mess) ;
%   - Input parameters
%           - key   : Cesar key 
%           - mess  : Message to decode 
%   - Output parameters
%           - messDec : Decoded message
function messDec = cesarDecode(key,mess) 
    messDec = mod( mess  - key, 255);
end


