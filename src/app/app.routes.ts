import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { ActivateAccountComponent } from './activate-account/activate-account.component';
import { TestComponent } from './test/test.component';
import { HomeComponent } from './home/home.component';
import { EvaluationsComponent } from './evaluations/evaluations.component';
import { ReponseEtudiantComponent } from './reponseetudiant/reponseetudiant.component';
import { ImpressionComponent } from './impression/impression.component';
import { ReponseJusteComponent } from './reponsejuste/reponsejuste.component';
import { TestGroupeComponent } from './test-groupe/test-groupe.component';
import { EtudiantComponent } from './etudiant/etudiant.component';
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

export const routes: Routes = [
  // Routes principales
  { path: '', component: HomeComponent },
  { path: 'home', component: HomeComponent },
  
  // Routes d'authentification
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'activate-account/:token', component: ActivateAccountComponent },
  
  // Routes des évaluations
  { path: 'evaluations', component: EvaluationsComponent },
  { path: 'test', component: TestComponent },
  { path: 'reponseetudiant', component: ReponseEtudiantComponent },
  { path: 'reponsejuste', component: ReponseJusteComponent },
  { path: 'impression/:testId/:groupeId', component: ImpressionComponent },
  
  // Routes de gestion des étudiants
  { path: 'students', component: EtudiantComponent },
  { path: 'students/add', component: AddstudentComponent },
  { path: 'students/update/:id', component: UpdateStudentComponent },
  { path: 'students/score/:id', component: ScoreStudentComponent },
  { path: 'students/upload', component: UploadStudentsComponent },
  
  // Routes de gestion des groupes et promotions
  { path: 'classes', component: TestGroupeComponent },
  { path: 'sites', component: SiteComponent },
  { path: 'promotions', component: PromotionComponent },
  { path: 'promotions/add', component: AddPromoComponent },
  { path: 'promotions/update/:id', component: UpdatePromoComponent },
  { path: 'groups', component: GroupeComponent },
  { path: 'groups/add', component: AddGroupComponent },
  { path: 'groups/update/:id', component: UpdateGroupComponent },

  // Route par défaut - redirige vers la page d'accueil
  { path: '**', redirectTo: '', pathMatch: 'full' }
];
