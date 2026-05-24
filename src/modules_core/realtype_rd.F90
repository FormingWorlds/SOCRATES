! *****************************COPYRIGHT*******************************
! (C) Crown copyright Met Office. All rights reserved.
! For further details please refer to the file COPYRIGHT.txt
! which you should have received as part of this distribution.
! *****************************COPYRIGHT*******************************

! Module to set the precision of real variables.

MODULE realtype_rd

  IMPLICIT NONE

  ! Internal Real precision within Socrates
  ! Single precision: SELECTED_REAL_KIND(6, 37)
  ! Double precision: SELECTED_REAL_KIND(15, 307)
#ifdef SINGLE_PRECISION
  INTEGER, PARAMETER :: RealK=SELECTED_REAL_KIND(6, 37)
#else
  INTEGER, PARAMETER :: RealK=SELECTED_REAL_KIND(15, 307)
#endif

  ! External Real precision for variables passed through the Runes interface
#ifdef SINGLE_PRECISION
  INTEGER, PARAMETER :: RealExt=SELECTED_REAL_KIND(6, 37)
#else
  INTEGER, PARAMETER :: RealExt=SELECTED_REAL_KIND(15, 307)
#endif

END MODULE realtype_rd
