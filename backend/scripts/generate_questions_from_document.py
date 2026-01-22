"""
Generate practice questions from PDF or HTML documents using AWS Bedrock.

This script:
1. Extracts text from PDF or HTML files
2. Uses AWS Bedrock Claude to generate questions
3. Saves questions to DynamoDB with proper source references

Usage:
    python scripts/generate_questions_from_document.py path/to/document.pdf --document-name "Name" --category "French History" --topic-id "hist-005"
    python scripts/generate_questions_from_document.py path/to/document.html --document-name "Name" --category "French Culture" --topic-id "cult-005"
"""

import sys
import os
import json
import uuid
import argparse
import boto3
from datetime import datetime, timezone
from typing import List, Dict, Any
from pathlib import Path

# PDF parsing
try:
    import PyPDF2
except ImportError:
    print("PyPDF2 not installed. Installing...")
    os.system(f"{sys.executable} -m pip install PyPDF2")
    import PyPDF2

# HTML parsing
try:
    from bs4 import BeautifulSoup
except ImportError:
    print("beautifulsoup4 not installed. Installing...")
    os.system(f"{sys.executable} -m pip install beautifulsoup4")
    from bs4 import BeautifulSoup

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from models.question import Question, QuestionSourceReference, AnswerOption
from repositories.question_repository import QuestionRepository
from shared.constants import QuestionType, GeneratedBy, Difficulty


# Initialize Bedrock client
bedrock_runtime = boto3.client('bedrock-runtime', region_name=os.getenv('AWS_REGION', 'us-east-1'))


def extract_text_from_pdf(pdf_path: str) -> Dict[int, str]:
    """Extract text from PDF, organized by page."""
    print(f"📖 Extracting text from PDF: {pdf_path}...")

    page_texts = {}
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)
        print(f"   Found {num_pages} pages")

        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            page_texts[page_num + 1] = text  # 1-indexed

    print(f"✅ Extracted text from {len(page_texts)} pages\n")
    return page_texts


def extract_text_from_html(html_path: str) -> Dict[int, str]:
    """Extract text from HTML file."""
    print(f"📖 Extracting text from HTML: {html_path}...")

    with open(html_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove script and style elements
    for script in soup(['script', 'style', 'nav', 'header', 'footer']):
        script.decompose()

    # Get text
    text = soup.get_text(separator='\n\n', strip=True)

    # Clean up whitespace
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    text = '\n\n'.join(lines)

    print(f"   Extracted {len(text)} characters")
    print(f"✅ Text extraction complete\n")

    # HTML doesn't have page numbers, so return as single "page"
    return {1: text}


def extract_text(file_path: str) -> Dict[int, str]:
    """
    Extract text from document (PDF or HTML).

    Returns:
        Dictionary mapping page number to text content
    """
    file_ext = Path(file_path).suffix.lower()

    if file_ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif file_ext in ['.html', '.htm']:
        return extract_text_from_html(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_ext}. Use .pdf, .html, or .htm")


def chunk_text(page_texts: Dict[int, str], chunk_size: int = 3000) -> List[Dict[str, Any]]:
    """Break text into manageable chunks for AI processing."""
    chunks = []
    current_chunk = ""
    current_pages = []

    for page_num, text in page_texts.items():
        # If adding this page would exceed chunk size, save current chunk
        if len(current_chunk) + len(text) > chunk_size and current_chunk:
            chunks.append({
                'text': current_chunk,
                'pages': current_pages.copy()
            })
            current_chunk = ""
            current_pages = []

        current_chunk += f"\n\n--- Page {page_num} ---\n\n{text}"
        current_pages.append(page_num)

    # Add final chunk
    if current_chunk:
        chunks.append({
            'text': current_chunk,
            'pages': current_pages
        })

    return chunks


def generate_questions_with_bedrock(
    chunk: Dict[str, Any],
    document_name: str,
    category: str,
    model_id: str = "anthropic.claude-3-5-sonnet-20241022-v2:0"
) -> List[Dict[str, Any]]:
    """Use AWS Bedrock Claude to generate questions from a text chunk."""
    prompt = f"""You are creating practice questions for the French civics naturalization test based on official study materials.

IMPORTANT: All questions, answers, and explanations MUST be written in French.

Document: {document_name}
Category: {category}
Pages: {chunk['pages'][0]}-{chunk['pages'][-1]}

Content:
{chunk['text']}

Generate 3-5 high-quality multiple choice questions based on this content. For each question:

1. Focus on important factual information that would appear on a civics test. Below is a list of 
official questions. If the answer to one (or more) appears in the document, use that question and 
find the answer in the document.
2. Write the question in French
3. Create 4 answer options (a, b, c, d) in French with exactly one correct answer
4. Provide a clear explanation in French referencing the source material
5. Identify a specific section/topic title from the content
6. Assign difficulty: 1 (easy), 2 (medium), or 3 (hard)
 
-- START OF LIST OF OFFICIAL QUESTIONS -- 
- Parmi les propositions suivantes, laquelle constitue une participation citoyenne ?
- Que garantit la liberté d’expression ?
- À quoi sert un titre de séjour ?
- La liberté de circulation permet à toute personne de :
- Sur quel site internet peut-on retrouver le symbole de la République française ?
- Complétez ces paroles de la Marseillaise : "Aux armes […] ! Formez vos bataillons"
- Complétez les paroles de la Marseillaise : "Allons enfants de la patrie […]"
- En application de la liberté individuelle, quelle proposition est correcte ? Une personne peut :
- Concernant la pratique de la religion, quelle proposition est correcte ?
- En tant que parent, peut-on refuser que son enfant participe aux cours de sport à l'école car ils sont mixtes ?
- Quelle est la devise de la France ?
- La répudiation de sa femme est :
- Les impôts permettent de financer les dépenses publiques. Quelle proposition est correcte ?
- Peut-on brûler publiquement un drapeau français ? 
- Que fait l’État pour lutter contre les discriminations ?
- Que représente Marianne ?
- Qu'est-ce que la liberté d'association ?
- Qu'est-ce que la liberté ?
- Qu'est-ce que la Marseillaise ?
- Sur quel document peut-on voir Marianne ?
- Un employeur refuse d’embaucher des femmes dans son entreprise. Que dit la loi ?
- Une des valeurs de la devise républicaine est l'égalité. Qu'est-ce que cela signifie ?
- Quelle est la place de la langue française dans la République ?
- Quels sont des symboles officiels de la République française ?
- A-t-on le droit d'insulter publiquement quelqu’un parce qu’il est différent (handicap, apparence physique, sexe…) ?
- Le régime de la France est :
- Pourquoi le principe de laïcité doit-il être respecté à l'école ?
- En quelle année la loi de séparation des Églises et de l'Etat a-t-elle été votée ?
- Une personne a-t-elle le droit de ne pas croire en une religion ?
- Quel droit est garanti par la laïcité ?
- À l'école publique, qui peut porter des signes religieux très visibles ?
- Selon le principe de laïcité, que signifie la neutralité de l’État ?
- Que peut faire un usager du service public dans une mairie ?
- Qui doit respecter le principe de neutralité religieuse dans une préfecture ?
- La laïcité impose-t-elle aux agents publics d'être neutres vis-à-vis des usagers ?
- Que garantit le principe de laïcité ?
- A-t-on le droit de changer de religion ?
- Que représente la laïcité ?
- Qu'est ce qui est interdit par la Charte de la laïcité à l'école ?
- Que dit l'article 1er de la Constitution française ?
- Système institutionnel et politique :

- Qu'est-ce que l'État de droit ?
- Le président de la République a commis un crime. Quelle proposition est correcte ?
- La loi est l'expression de : 
- Quelle est la durée du mandat du conseil municipal et du maire ?
- Que garantit l’État de droit ?
- Une personne peut-elle voter à la place d'une autre ?
- Est-ce que le vote est obligatoire ?
- À la fin de son mandat, le président de la République peut-il décider de rester au pouvoir ?
- Qui dirige l'action du Gouvernement ?
- Qui nomme le Premier ministre ?
- Quelle est l'organisation administrative de la France ?
- Qu'est-ce que le pouvoir législatif ? Le pouvoir :
- Pourquoi séparer les trois pouvoirs dans une démocratie ?
- Qui sanctionne l'auteur d'un vol ?
- Quel est le rôle du gouvernement ?
- Que se passe-t-il si un ministre ne respecte pas la loi ?
- Combien de députés composent l’Assemblée nationale ?
- Qui peut voter aux élections en France ?
- Pour combien de temps sont élus les sénateurs ?
- La séparation des pouvoirs est un principe fondamental. Quels sont les trois pouvoirs concernés ?
- Est-ce que le président de la République a tous les pouvoirs ?
- Qui est le préfet ?
- Quelle condition est nécessaire pour voter aux élections ?
- Qui dirige la commune ?
- Quel est le régime politique de la France aujourd'hui ?
- Qu'est-ce que l'Hôtel de Matignon ?
- Le Parlement est composé :
- Quel est le rôle du président de la République ?
- Quel est le rôle du Premier ministre ?
- Qui est le chef du Gouvernement ?
- Combien y a-t-il de régions en France ?
- Quel est le rôle du Défenseur des droits ?
- Depuis quand l'euro est-elle la monnaie unique ?
- Quel est le rôle principal du département ?
- Quel est le rôle principal des communes ?
- Combien de communes environ existe-t-il en France ?
- Quel traité concerne la construction de l'Union européenne ?
- Quel État a quitté l'Union européenne en 2020 ?
- Quelle est la devise de l’Union européenne ?
- Quel est l'hymne de l'Union européenne ?
- De quoi est composé le drapeau européen ?
- De quelle couleur est le drapeau européen ?
- En quelle année le traité de Maastricht, qui marque la fondation de l'Union européenne, a-t-il été signé ?
- Où est le siège du Parlement européen ?
- Où est le siège de la Commission européenne ?
- Quel État n'est pas membre de l'Union européenne ?
- Quand célèbre-t-on la journée de l'Europe ?
- À quelle fréquence les élections européennes sont-elles organisées ?
- Quelle condition est nécessaire pour voter aux élections européennes ?
- Quel pays est un pays fondateur de l'Union européenne ?
- Droits et devoirs :

- À quelle liberté la PMA fait-elle référence ?
- Au nom de quoi l'État justifie-t-il la restriction des droits ?
- Concernant le droit de se marier, quelle proposition est correcte ?
- Est-il toujours possible de divorcer ?
- La peine de mort est :
- Laquelle de ces citations est inscrite dans la Déclaration des Droits de l'homme et du Citoyen de 1789 ?
- Le recours à l'avortement est-il autorisé ?
- Que contient la Constitution ?
- Que garantit la liberté de la presse ?
- Que prévoit la Charte de l'environnement ?
- Que signifie la dignité humaine ?
- Que signifie le droit de manifester ?
- Que signifie PMA ?
- Quel texte est le plus difficile à modifier ?
- Quelle liberté permet à une personne de croire en la religion de son choix ?
- Qu'est-ce que le droit de grève ?
- Qu'est-ce que la Constitution ?
- Qui peut demander à avorter ?
- Une femme majeure de nationalité française a-t-elle le droit de voter aux élections ?
- Concernant l'utilisation des réseaux sociaux, quelle proposition est correcte ?
- Jeter un mégot par terre est :
- L'État peut-il limiter les droits et libertés ?
- Parmi ces actions, laquelle permet d'adopter une attitude respectueuse de l’environnement ?
- Quelle proposition constitue une obligation ?
- Pour quel motif peut-on limiter la liberté d'expression ?
- Pourquoi doit-on trier ses déchets ?
- Que doit faire une victime de violences ?
- Que doit-on faire face aux ordres des policiers ou gendarmes ?
- Quel est le rôle de la police ?
- Quel est un exemple d’assistance à personne en danger ?
- Quel exemple illustre une limitation de liberté pour protéger l'intérêt général ?
- Quelle est l’attitude à avoir lorsque qu'on est témoin de violences ?
- Quelle est l'infraction la plus grave ?
- Quelle obligation concerne toutes les personnes résidant en France quelle que soit leur nationalité ?
- Quelle proposition représente un exemple de crime ?
- Quelle proposition représente un exemple de délit ?
- Qui veille au maintien de l’ordre public ?
- S'agissant des déchets, quelle proposition est correcte ?
- Histoire géographie et culture :

- Quel était le surnom de Louis XIV ?
- Quel roi de France a été exécuté pendant la Révolution française ?
- En quelle année Napoléon Ier est-il devenu empereur ?
- Lequel de ces personnages a un lien avec la République française ?
- De quand date l'appel à la résistance du général de Gaulle ?
- Pourquoi la Shoah est-elle étudiée à l'école ?
- Quel pays a été colonisé par la France ?
- Depuis quand les Français élisent-ils le président de la République au suffrage universel direct ?
- Quelle est la première étape de la construction européenne en 1951 ?
- Durant le mandat de quel président la peine de mort a-t-elle été abolie ?
- Quel régime politique a été mis en place pendant la Révolution française en 1792 ?
- Qui était une figure de la Résistance française pendant la Seconde Guerre mondiale ?
- En 1944, qu'est-ce qui a changé pour les femmes ?
- Quelle organisation internationale a été créée en 1945 après la Seconde Guerre mondiale ?
- Quelle peine a été supprimée en 1981 ?
- En quelle année l'euro est-elle devenue la monnaie utilisée en France ?
- En quelle année a commencé la Première Guerre mondiale ?
- Où a eu lieu le débarquement en 1944 ?
- Quel continent a été le plus concerné par la décolonisation française après la Seconde Guerre mondiale ?
- Que fête-t-on le 8 mai ?
- Quelle mer ou océan borde la France métropolitaine ?
- Quel pays a une frontière terrestre avec la France métropolitaine ?
- Quelle ville française est un port maritime ?
- Quelle mer se situe entre la France et l'Angleterre ?
- Qu'est ce que la France d'outre-mer ?
- Quelle chaîne de montagnes est située entre la France et l’Espagne ?
- Quelle île française se trouve dans l'océan Indien ?
- Quelle est la population approximative de la France en 2025 ?
- Quel fleuve traverse Paris ?
- Lequel de ces pays partage des frontières terrestres avec la France ?
- Quel pays a une frontière avec la France métropolitaine au nord-est ?
- Où se trouvent les principales activités économiques en France ?
- Parmi ces pays, lequel attire le plus de visiteurs chaque année ?
- Où habite la majorité des Français ?
- Quelle région est la plus peuplée ?
- Quelle ville française fait partie des 10 plus grandes métropoles du pays ?
- Lequel de ces départements de France est le plus touristique ?
- Quand peut-on visiter gratuitement des lieux culturels en France ?
- Combien de personnes parlent français dans le monde ?
- Qui était Marguerite Yourcenar ?
- Quel peintre est français ?
- Quel musée est situé à Paris ?
- Qui était Auguste Rodin ?
- Quel est le classement de la langue française parmi les langues les plus parlées dans le monde ?
- Quelle cathédrale célèbre a été en partie détruite par un incendie en 2019 ?
- Qui était une écrivaine française célèbre ?
- Qui était un célèbre musicien français ?
- Qui était Auguste Renoir ?
- Quelle fête est française ?
- Vivre dans la société française :

- Quel mariage est reconnu par l'État ?
- Auprès de quelle institution les parents peuvent-ils inscrire leur enfant à l'école publique ?
- En cas de divorce, qui exerce l'autorité parentale ?
- Quelle aide permet aux personnes qui ont des difficultés financières d'avoir un avocat ? 
- Où faut-il déclarer la naissance d'un enfant ?
- Quelle est l'une des conditions pour passer l'examen du permis de conduire ?
- Un bail locatif est valide s'il est :
- Où peut-on déposer un lave-vaisselle cassé ?
- Quel numéro d'urgence permet d'appeler la police ?
- Concernant l'accès aux soins, quelle proposition est correcte ?
- À qui est accessible la contraception ?
- Qu’est-ce que le principe de confidentialité dans le domaine de la santé ?
- L'inscription à l'Assurance maladie est :
- Qui peut demander un congé parental d'éducation ?
- Quelles sont les affaires traitées par le conseil de prud'hommes ?
- Travailler sans être déclaré est :
- Lorsqu'un employeur veut qu'un salarié travaille plus longtemps que la durée prévue dans le contrat de travail :
- Quelle est la mission de France Travail ?
- Dans une entreprise, le droit syndical permet :
- Dans une entreprise, le droit de grève autorise :
- Quelles sont les conditions pour toucher les allocations chômage ?
- Qu'est-ce que l'école maternelle ?
- Comment s'appelle le diplôme passé par les élèves à la fin du collège ?
- Les parents d'élève ont le droit de :
- Qui peut manger à la cantine scolaire ?
- À quel âge commence l'instruction obligatoire des enfants ?
- Quel est l'âge de la majorité ?
- À l'école, il est interdit aux parents de :
- Quel motif d'absence est accepté par l'école ?
- Des parents ne respectent pas l'obligation d'instruction pour leurs enfants. Quelle sanction maximale risquent-ils ?
- Quand ont lieu les vacances scolaires de Noël ?
 
-- END OF LIST OF OFFICIAL QUESTIONS -- 

Return ONLY valid JSON in this exact format (no markdown, no code blocks):
{{ 
  "questions": [
    {{
     "question_text": "Question en français?",
     "answer_options": [
        {{"id": "a", "text": "Option A en français"}},
        {{"id": "b", "text": "Option B en français"}},
        {{"id": "c", "text": "Option C en français"}},
        {{"id": "d", "text": "Option D en français"}}
      ],
      "correct_answer": "a",
      "explanation": "Explication en français",
      "difficulty": 1,
      "section": "Section name from document",
      "page": {chunk['pages'][0]}
    }}
  ]
}}"""

    print(f"   🤖 Generating questions for pages {chunk['pages'][0]}-{chunk['pages'][-1]}...")

    # Bedrock request body
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4096,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            body=json.dumps(request_body)
        )

        response_body = json.loads(response['body'].read())
        response_text = response_body['content'][0]['text'].strip()

        # Parse JSON response
        result = json.loads(response_text)
        print(f"   ✅ Generated {len(result['questions'])} questions")
        return result['questions']

    except json.JSONDecodeError as e:
        print(f"   ⚠️  Error parsing AI response: {e}")
        print(f"   Response was: {response_text[:200]}...")
        return []
    except Exception as e:
        print(f"   ❌ Error calling Bedrock: {e}")
        return []


def create_question_objects(
    ai_questions: List[Dict[str, Any]],
    document_name: str,
    category: str,
    topic_id: str
) -> List[Question]:
    """Convert AI-generated questions to Question objects."""
    questions = []
    timestamp = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

    for q in ai_questions:
        question = Question(
            question_id=str(uuid.uuid4()),
            topic_id=topic_id,
            category=category,
            question_text=q['question_text'],
            question_type=QuestionType.MULTIPLE_CHOICE,
            correct_answer=q['correct_answer'],
            explanation=q['explanation'],
            difficulty=q['difficulty'],
            source_reference=QuestionSourceReference(
                document=document_name,
                page=q['page'],
                section=q['section']
            ),
            generated_by=GeneratedBy.AI,
            validated=False,  # Needs manual review
            created_at=timestamp,
            answer_options=[
                AnswerOption(id=opt['id'], text=opt['text'])
                for opt in q['answer_options']
            ]
        )
        questions.append(question)

    return questions


def main():
    parser = argparse.ArgumentParser(description='Generate questions from PDF or HTML using AWS Bedrock')
    parser.add_argument('file_path', help='Path to PDF or HTML file')
    parser.add_argument('--document-name', required=True, help='Name of the document')
    parser.add_argument('--category', required=True, help='Category (e.g., "French History")')
    parser.add_argument('--topic-id', required=True, help='Topic ID (e.g., "hist-005")')
    parser.add_argument('--max-chunks', type=int, default=None, help='Max chunks to process (for testing)')
    parser.add_argument('--preview-only', action='store_true', help='Preview questions without saving')
    parser.add_argument('--model-id', default='anthropic.claude-3-5-sonnet-20241022-v2:0', help='Bedrock model ID')

    args = parser.parse_args()

    # Check file exists
    if not os.path.exists(args.file_path):
        print(f"❌ Error: File not found: {args.file_path}")
        sys.exit(1)

    file_type = Path(args.file_path).suffix.upper()

    print("=" * 60)
    print(f"French Civics Question Generator (AWS Bedrock)")
    print("=" * 60 + "\n")
    print(f"📄 Document: {args.document_name}")
    print(f"📁 File: {args.file_path} ({file_type})")
    print(f"🏷️  Category: {args.category}")
    print(f"🆔 Topic ID: {args.topic_id}")
    print(f"🤖 Model: {args.model_id}\n")

    # Extract text from document
    try:
        page_texts = extract_text(args.file_path)
    except Exception as e:
        print(f"❌ Error extracting text: {e}")
        sys.exit(1)

    # Chunk text for AI processing
    chunks = chunk_text(page_texts)
    print(f"📦 Created {len(chunks)} text chunks for processing\n")

    # Limit chunks if specified
    if args.max_chunks:
        chunks = chunks[:args.max_chunks]
        print(f"⚠️  Processing only first {len(chunks)} chunks (--max-chunks)\n")

    # Generate questions for each chunk
    all_questions = []
    for i, chunk in enumerate(chunks, 1):
        print(f"Processing chunk {i}/{len(chunks)}...")
        ai_questions = generate_questions_with_bedrock(
            chunk,
            args.document_name,
            args.category,
            args.model_id
        )

        if ai_questions:
            question_objects = create_question_objects(
                ai_questions,
                args.document_name,
                args.category,
                args.topic_id
            )
            all_questions.extend(question_objects)

        print()

    print(f"\n✨ Generated {len(all_questions)} total questions\n")

    # Preview questions
    if all_questions:
        print("=" * 60)
        print("PREVIEW OF GENERATED QUESTIONS")
        print("=" * 60)
        for i, q in enumerate(all_questions[:3], 1):
            print(f"\n{i}. {q.question_text}")
            for opt in q.answer_options:
                marker = "✓" if opt.id == q.correct_answer else " "
                print(f"   [{marker}] {opt.id}. {opt.text}")
            print(f"   Explanation: {q.explanation}")
            print(f"   Source: {q.source_reference.document}, p.{q.source_reference.page}, {q.source_reference.section}")
            print(f"   Difficulty: {q.difficulty}")

        if len(all_questions) > 3:
            print(f"\n   ... and {len(all_questions) - 3} more questions")
        print("\n" + "=" * 60)

    # Save to database
    if not args.preview_only and all_questions:
        response = input(f"\n💾 Save {len(all_questions)} questions to database? (yes/no): ")
        if response.lower() in ['yes', 'y']:
            print("\n🚀 Saving questions to DynamoDB...")
            repo = QuestionRepository()
            repo.batch_create(all_questions)
            print(f"✅ Successfully saved {len(all_questions)} questions!")
            print("\n⚠️  Note: Questions are marked as 'validated=False' and need manual review")
            print("   Run: python scripts/validate_generated_questions.py")
        else:
            print("❌ Cancelled - questions not saved")
    elif args.preview_only:
        print("\n👀 Preview mode - questions not saved")

    print("\n✨ Done!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
