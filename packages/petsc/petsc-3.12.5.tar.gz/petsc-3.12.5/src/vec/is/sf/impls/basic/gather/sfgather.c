#include <../src/vec/is/sf/impls/basic/gatherv/sfgatherv.h>

#define PetscSFPackGet_Gather PetscSFPackGet_Allgatherv

/* Reuse the type. The difference is some fields (i.e., displs, recvcounts) are not used in Gather, which is not a big deal */
typedef PetscSF_Allgatherv PetscSF_Gather;

PETSC_INTERN PetscErrorCode PetscSFBcastAndOpBegin_Gather(PetscSF sf,MPI_Datatype unit,PetscMemType rootmtype,const void *rootdata,PetscMemType leafmtype,void *leafdata,MPI_Op op)
{
  PetscErrorCode       ierr;
  PetscSFPack          link;
  PetscMPIInt          rank,sendcount;
  MPI_Comm             comm;
  char                 *recvbuf;

  PetscFunctionBegin;
  ierr = PetscSFPackGet_Gather(sf,unit,rootmtype,rootdata,leafmtype,leafdata,&link);CHKERRQ(ierr);
  ierr = PetscObjectGetComm((PetscObject)sf,&comm);CHKERRQ(ierr);

  if (op == MPIU_REPLACE) {
    recvbuf = (char*)leafdata;
  } else {
    ierr = MPI_Comm_rank(comm,&rank);CHKERRQ(ierr);
    if (!link->leafbuf[leafmtype] && !rank) {ierr = PetscMallocWithMemType(leafmtype,sf->nleaves*link->unitbytes,(void**)&link->leafbuf[leafmtype]);CHKERRQ(ierr);}
    recvbuf = link->leafbuf[leafmtype];
  }

  ierr = PetscMPIIntCast(sf->nroots,&sendcount);CHKERRQ(ierr);
  ierr = MPIU_Igather(rootdata,sendcount,unit,recvbuf,sendcount,unit,0/*rank 0*/,comm,link->rootreqs[PETSCSF_ROOT2LEAF_BCAST][rootmtype]);CHKERRQ(ierr);
  PetscFunctionReturn(0);
}

static PetscErrorCode PetscSFReduceBegin_Gather(PetscSF sf,MPI_Datatype unit,PetscMemType leafmtype,const void *leafdata,PetscMemType rootmtype,void *rootdata,MPI_Op op)
{
  PetscErrorCode       ierr;
  PetscSFPack          link;
  PetscMPIInt          recvcount;
  MPI_Comm             comm;
  void                 *recvbuf;

  PetscFunctionBegin;
  ierr = PetscSFPackGet_Gather(sf,unit,rootmtype,rootdata,leafmtype,leafdata,&link);CHKERRQ(ierr);
  ierr = PetscObjectGetComm((PetscObject)sf,&comm);CHKERRQ(ierr);

  if (op == MPIU_REPLACE) {
    recvbuf = (char*)rootdata;
  } else {
    if (!link->rootbuf[rootmtype]) {ierr = PetscMallocWithMemType(rootmtype,sf->nroots*link->unitbytes,(void**)&link->rootbuf[rootmtype]);CHKERRQ(ierr);}
    recvbuf = link->rootbuf[rootmtype];
  }

  ierr = PetscMPIIntCast(sf->nroots,&recvcount);CHKERRQ(ierr);
  ierr = MPIU_Iscatter(leafdata,recvcount,unit,recvbuf,recvcount,unit,0/*rank 0*/,comm,link->rootreqs[PETSCSF_LEAF2ROOT_REDUCE][rootmtype]);CHKERRQ(ierr);
  PetscFunctionReturn(0);
}

PETSC_INTERN PetscErrorCode PetscSFCreate_Gather(PetscSF sf)
{
  PetscErrorCode  ierr;
  PetscSF_Gather  *dat = (PetscSF_Gather*)sf->data;

  PetscFunctionBegin;
  /* Inherit from Allgatherv */
  sf->ops->Reset           = PetscSFReset_Allgatherv;
  sf->ops->Destroy         = PetscSFDestroy_Allgatherv;
  sf->ops->GetGraph        = PetscSFGetGraph_Allgatherv;
  sf->ops->GetRootRanks    = PetscSFGetRootRanks_Allgatherv;
  sf->ops->GetLeafRanks    = PetscSFGetLeafRanks_Allgatherv;
  sf->ops->BcastAndOpEnd   = PetscSFBcastAndOpEnd_Allgatherv;
  sf->ops->ReduceEnd       = PetscSFReduceEnd_Allgatherv;
  sf->ops->FetchAndOpEnd   = PetscSFFetchAndOpEnd_Allgatherv;
  sf->ops->CreateLocalSF   = PetscSFCreateLocalSF_Allgatherv;

  /* Inherit from Gatherv */
  sf->ops->FetchAndOpBegin = PetscSFFetchAndOpBegin_Gatherv;

  /* Gather stuff */
  sf->ops->BcastAndOpBegin = PetscSFBcastAndOpBegin_Gather;
  sf->ops->ReduceBegin     = PetscSFReduceBegin_Gather;

  ierr     = PetscNewLog(sf,&dat);CHKERRQ(ierr);
  sf->data = (void*)dat;
  PetscFunctionReturn(0);
}

