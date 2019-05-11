
int plusprochevoisin (int i)
{ 
    int j,jmin; 
    long int dist2, distmin=900000000;
    for(j=0;j<N;j++) if (i!=j)
        { 
            dist2=(x[i]-x[j])*(x[i]-x[j])+(y[i]-y[j])*(y[i]-y[j]); 
            if (dist2<distmin) {distmin=dist2; jmin=j; }
        }
        return jmin;
} 

int voisinsuivantgauche(int i,int j)
{ 
    int k;

    int v1x,v1y,v2x,v2y,numerovoisin=-1;

    double prodscal,longki2,longki,longkj2,longkj,coskij,cosmin,det;

    cosmin=1.;

    for(k=0;k<N;k++) if (k!=i && k!=j)

        { v1x=x[j]-x[i],v1y=y[j]-y[i]; v2x=x[k]-x[i],v2y=y[k]-y[i]; det=v1x*v2y-v1y*v2x;
            if (det<0) /* on cherche un point à droite */
                { 
                    prodscal= (double)(x[i]-x[k])*(double)(x[j]-x[k])+(double)(y[i]-y[k])*(double)(y[j]-y[k]);

                    longki2=(double)(x[i]-x[k])*(double)(x[i]-x[k])+(double)(y[i]-y[k])*(double)(y[i]-y[k]);

                    longkj2=(double)(x[j]-x[k])*(double)(x[j]-x[k])+(double)(y[j]-y[k])*(double)(y[j]-y[k]);

                    longki=sqrt(longki2); longkj=sqrt(longkj2);

                    coskij=prodscal/(longki*longkj); /* on veut le cosinus le plus petit possible */

                    if (coskij<cosmin) {
                        cosmin=coskij; numerovoisin=k;
                    }
                }
        }
    return numerovoisin;
}

int voisinsuivantdroite(int i,int j)
{ 
    int k;

    int v1x,v1y,v2x,v2y,numerovoisin=-1;

    double prodscal,longki2,longki,longkj2,longkj,coskij,cosmin,det;

    cosmin=1.;

    for(k=0;k<N;k++) if (k!=i && k!=j)

        { v1x=x[j]-x[i],v1y=y[j]-y[i]; v2x=x[k]-x[i],v2y=y[k]-y[i]; det=v1x*v2y-v1y*v2x;
            if (det>0) /* on cherche un point à droite */
                { 
                    prodscal= (double)(x[i]-x[k])*(double)(x[j]-x[k])+(double)(y[i]-y[k])*(double)(y[j]-y[k]);

                    longki2=(double)(x[i]-x[k])*(double)(x[i]-x[k])+(double)(y[i]-y[k])*(double)(y[i]-y[k]);

                    longkj2=(double)(x[j]-x[k])*(double)(x[j]-x[k])+(double)(y[j]-y[k])*(double)(y[j]-y[k]);

                    longki=sqrt(longki2); longkj=sqrt(longkj2);

                    coskij=prodscal/(longki*longkj); /* on veut le cosinus le plus grand possible */

                    if (coskij<cosmin) {
                        cosmin=coskij; numerovoisin=k;
                    }
                }
        }
    return numerovoisin;
}

void main(){
    for(i=0;i<N;i++) /* on prend chaque site */
        { ppv=plusprochevoisin(i); voisins[i][0]=ppv; longueur[i]=1; kk=0;
 do { vsd=voisinsuivantdroite(i,voisins[i][kk]); longueur[i]++; voisins[i][kk+1]=vsd; kk++;
 }
 while(vsd!=ppv && vsd!=-1);
 if (vsd==-1)
 { envconv[i]=1;
 do { vsg=voisinsuivantgauche(i,voisins[i][0]);
 if (vsg!=-1)
 { for(kkk=longueur[i]-1;kkk>=0;kkk--) voisins[i][kkk+1]=voisins[i][kkk];
 voisins[i][0]=vsg; longueur[i]++;
 }
 }
 while(vsg!=-1);
 }
 }
 for(i=0;i<N;i++) /* dessin des triangles autour de i */
 for(ii=0;ii<longueur[i]-1;ii++) if (voisins[i][ii+1]!=-1)
 { line(x[i],yorig-y[i],x[voisins[i][ii]],yorig-y[voisins[i][ii]],blue);
 line(x[i],yorig-y[i],x[voisins[i][ii+1]],yorig-y[voisins[i][ii+1]],blue);
 line(x[voisins[i][ii]],yorig-y[voisins[i][ii]],x[voisins[i][ii+1]],
 yorig-y[voisins[i][ii+1]],blue);
 } 
}