
Set Printing Projections.


Require Export Ensembles.

Section group_stuff.

Variable U:Type.


Record group :=
  {
    S : Ensemble U;
    id : U;
    op : U -> U -> U;
    inv : U -> U;
    closed : forall (x y :U), In U S x -> In U S y -> In U S (op x y);
    inv_exists: forall (x : U), In U S x -> In U S (inv x);
    op_id_l : forall x:U, In U S x -> (op id x) = x;
    op_id_r : forall x:U, In U S x -> (op x id) = x;
    op_assoc : forall (x y z:U), op x (op y z) = op (op x y) z;
    op_inv_l : forall (x:U), In U S x -> op (inv x) x = id;
    op_inv_r : forall (x:U), In U S x -> op x (inv x) = id;
  }.

Definition is_group (S':Ensemble U) (id':U) (op':U->U->U) (inv':U->U) :Prop :=
  exists G:group, (S G)=S' /\ (id G)=id' /\ (op G)=op' /\ (inv G)=inv'.

End group_stuff.





