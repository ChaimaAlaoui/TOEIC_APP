import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { ActivateAccountComponent } from './activate-account/activate-account.component';
import { TestComponent } from './test/test.component';
import { HomeComponent } from './home/home.component';
import { ClasseComponent } from './classe/classe.component';
import { EvaluationsComponent } from './evaluations/evaluations.component';
import { ReponseEtudiantComponent } from './reponseetudiant/reponseetudiant.component';
import { ImpressionComponent } from './impression/impression.component';
import { ReponseJusteComponent } from './reponsejuste/reponsejuste.component';
import { TestGroupeComponent } from './test-groupe/test-groupe.component';
import { EtudiantComponent } from './etudiant/etudiant.component';
import { Component, NgModule } from '@angular/core';
import { UpdateStudentComponent } from './etudiant/update-student/update-student.component';
import { ScoreStudentComponent } from './etudiant/score-student/score-student.component';
import { AddstudentComponent } from './etudiant/addstudent/addstudent.component';
import { UploadStudentsComponent } from './etudiant/upload-students/upload-students.component';
import { SiteComponent } from './site/site.component';
import { PromotionComponent } from './promotion/promotion.component';
import { GroupeComponent } from './groupe/groupe.component';
import { AddGroupComponent } from './groupe/addgroupe/addgroup/addgroup.component';
import { UpdateGroupComponent } from './groupe/updategroupe/updategroup/updategroup.component';
import { AddPromoComponent } from './promotion/addPromo/add-promo/add-promo.component';
import { UpdatePromoComponent } from './promotion/updatePromo/update-promo/update-promo.component';




// Définir les routes de l'application
export const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'register', component:  RegisterComponent },
  { path: '', redirectTo: '/login', pathMatch: 'full' } ,
  { path: 'activate-account/:token', component: ActivateAccountComponent },
  { path: 'test', component: TestComponent },
  { path: 'home', component: HomeComponent },
  { path: 'classe', component: ClasseComponent },
  { path: 'evaluations', component: EvaluationsComponent },
  { path: 'classes', component: TestGroupeComponent },
  { path: 'reponseetudiant', component: ReponseEtudiantComponent },
  { path: 'impression', component: ImpressionComponent },
  { path: 'reponsejuste', component: ReponseJusteComponent },
  { path: 'studentlist', component: EtudiantComponent },
  {path:'update-student/:id', component:UpdateStudentComponent},
  {path: 'scorestudent/:id',component:ScoreStudentComponent},
  {path:'addstudent', component:AddstudentComponent},
  {path:'uploadstudent',component:UploadStudentsComponent},
  {path:'site',component:SiteComponent},
  {path:'promotionlist',component:PromotionComponent},
  {path:'groupelist',component:GroupeComponent},
  {path:'addgroup',component:AddGroupComponent},
  {path:'updategroup/:id',component:UpdateGroupComponent},
  {path:'scorestudent',component:ScoreStudentComponent},
  { path: 'addpromo', component:AddPromoComponent },
  { path: 'updatepromo/:id',component:UpdatePromoComponent  }

];
