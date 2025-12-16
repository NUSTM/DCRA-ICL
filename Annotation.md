# Annotation Guidelines

A SOCP quadruple is defined as any sentence or clause in which:
* A subject smartphone (usually the phone being reviewed) is compared to
* An object smartphone (another phone mentioned in the same comment),
* with regard to a particular aspect category, and
* a preference direction is expressed (better/worse/equal).

We annotate only explicit comparisons between two phones with clear evaluative preferences.

We begin by introducing the full category taxonomy used for comparison labeling. 
Then, we detail the annotation schema. 
Finally, we describe how large language models were employed for annotation.

## Category System
<!--方面类别用于定义评论中所表达观点所涉及的方面类型。我们从针对笔记本电脑的 SemEval-2015 task 12中获得灵感，将其方面类别体系调整到智能手机领域。
该分类系统包含两种主要类型的标签：实体标签和属性标签。每个实体标签与属性标签的唯一组合会形成一个“方面类别”标签。
-->

The category defines the type of aspect involved in the opinion expressed in the review. 
We adapt the aspect category system from **SemEval-2015 Task 12 for laptops**(https://aclanthology.org/S15-2082/) to the smartphone domain. 
The category system comprises two primary types of labels: **Entity Labels** and **Attribute Labels**. Each unique pair of an entity and an attribute label defines an **Aspect Category Label**.

<!--
下面是 SemEval-2015 task 12 的真实样本：
The unibody design is edgy ➡ { LAPTOP#DESIGN_FEATURES, positive}
The screen is nice and the images comes very clear. ➡ {DISPLAY#GENERAL, positive} {DISPLAY#QUALITY, positive}
 
对于第一个样本 ，“unibody design” 明确描述的是笔记本的外观设计特征，没有具体指向某一部件，因此类别归为 LAPTOP#DESIGN_FEATURES。对于第二个样本， “screen is nice” 属于对屏幕整体的泛化评价，“images comes very clear” 强调的是视觉清晰度，属于屏幕显示效果，他们都指向了“屏幕”，但描述了不同的属性，因此类别分别是DISPLAY#GENERAL 和 DISPLAY#QUALITY。
可以看到，semeval在标注是遵循 “部件 + 属性” 的双层结构，优先匹配评论指向的具体实体 - 特征对。我们在标注的时候也是如此。

此外，我们结合京东平台对智能手机的官方评价维度，将laptop的分类体系适用于手机领域。京东平台的评价维度包括“外形外观”“拍照效果”“屏幕音效”等，可以看到，智能手机的关注点会突出拍照、屏幕、音效属性。因此，我们将实体CAMERA、AUDIO DEVICES从原始的MULTIMEDIA DEVICE中提取出来，而实体DISPLAY保留下来。从而，进一步提升了体系对真实电商场景的适配性，使类别标签能直接对应企业产品分析的关注维度。

下面介绍手机领域的类别标签体系：
-->
Below are real samples from SemEval-2015 Task 12:

1.  The unibody design is edgy ➡ {LAPTOP#DESIGN_FEATURES, positive}
2.  The screen is nice and the images comes very clear. ➡ {DISPLAY#GENERAL, positive} {DISPLAY#QUALITY, positive}
3. Hopefully Amazon will take this back. ➡ {LAPTOP#GENERAL, negative}
4.	The processor screams. ➡ {CPU#OPERATION_PERFORMANC, positive}

For the first example, “unibody design” clearly describes the design feature of the laptop's appearance, without pointing to a specific component; therefore, the category is labeled as LAPTOP#DESIGN_FEATURES. For the second example, “screen is nice” is a general evaluation of the screen as a whole, while “images come very clear” emphasizes visual clarity, which belongs to display quality. Both refer to the screen but describe different attributes, hence the categories are DISPLAY#GENERAL and DISPLAY#QUALITY, respectively.

For the third example, no specific component is mentioned; instead, there is dissatisfaction with the entire laptop, so it is categorized as LAPTOP#GENERAL. For the fourth example, “processor” explicitly refers to the CPU, and “screams” indicates that the laptop's performance is very strong, so it is labeled as CPU#OPERATION_PERFORMANCE.

As we can see, SemEval follows a two-level annotation structure of entity + attribute, prioritizing the matching of the specific entity pointed to by the comment and its corresponding feature. We follow the same approach in our annotation. Therefore, “better visual effects” focuses on the screen's display characteristics and is categorized under DISPLAY#QUALITY, rather than PHONE#DESIGN; “stronger processor” points to the processor's performance and is categorized under PROCESSOR#PERFORMANCE, rather than PHONE#GENERAL. This granularity ensures clarity of categories and maintains semantic consistency.

In addition, we incorporated the official evaluation dimensions of smartphones used on the JD.com platform, adapting the laptop-oriented classification scheme to the smartphone domain. JD.com highlights product aspects such as appearance and design, camera performance, and screen & audio quality. Accordingly, we extracted the entities CAMERA and AUDIO DEVICES from the original broader category MULTIMEDIA DEVICE, while retaining DISPLAY as an independent entity. This refinement improves the applicability of the scheme to real e-commerce scenarios, making the aspect labels directly align with the key dimensions that enterprises and customers focus on in product evaluation.


Introduction to the category labeling scheme in the smartphone domain:
<!--
实体标签可以是整部手机（例如 Apple iPhone 15）、手机的有形部分（例如屏幕）或抽象部分（例如分辨率），也可以是制造公司（例如 Apple）以及其提供的服务（例如售前及售后客户支持）。
属性标签表示与每个实体标签相关的特定的质量或特征。
下面表格展示了 16 个预定义的实体标签与 8 个预定义的属性标签，以及它们的描述。
-->
An entity label can refer to the whole phone (e.g. Apple iPhone 15), its tangible components (e.g. screen) and abstract parts (e.g. resolution), 
the manufacturing company (e.g. Apple) or the services it provides (e.g. pre- and after-sales customer support). 
An attribute label denotes the specific qualities or characteristics associated with each entity label. 
The following tables respectively show 16 predefined entity labels and 8 predefined attribute labels, along with their descriptions.
<br>
<br>
Entity Label(16) | Description
----| ----
PHONE | Phone as a whole.
DISPLAY | Display screen, external screen, internal screen, etc.
PROCESSOR | CPU.
MEMORY&STORAGE | Running memory and storage space.
CAMERA | Camera, front camera, rear camera, etc.
BATTERY&POWER | Battery and power supply (charger, charging cable).
COMMUNICATION | Internet connectivity (4G, 5G), Wi-Fi, Bluetooth, etc.
COOLING | Fans, cooling systems, radiators, etc.
AUDIO DEVICES | Sound, speakers, headphones, vibration motors, etc.
PHYSICAL INTERFACE | SIM card slot, physical buttons (power button, volume buttons), ports (Type-C port, Lightning port), and more.
ACCESSORY | Cell phone case, cell phone film, matching earphone, stylus and so on.
HARDWARE | Overall hardware configuration.
OS | Operating systems and their functions.
APP | Software applications, such as preinstalled apps (memos, settings, browser, etc.).
SERVICE | Pre- and post-sales customer support, customer service, repair services, product support, replacement policies and staff.
BRAND | Brands and Companies.

Attribute Label(8) | Description
----| ----
GENERAL | A general opinion about the entity as a whole (e.g., cell phone, screen) without focusing on any specific attributes.
PRICE | Price (cheap or expensive), value for money and cost of services provided by the manufacturer.
QUALITY | Precision in the construction and design of the product, durability and reliability under normal conditions of use.
PERFORMANCE | The operational efficiency and handling capacity of a product, especially under high loads or specific operating conditions.
USABILITY | Ease or convenience of use, learning, (un)installing, handling, operating, setting, navigating, updating, configuring, touching, etc., the experience of use as well as evaluating upgradability, compatibility, and ergonomics (focusing on the software features of the phone).
DESIGN | Appearance (shape, color, appearance), dimensions, weight, quantity, and ergonomics (focusing on the structural design of the phone), placement of components, software design, and warranty duration and terms/conditions.
FEATURES | (additional or missing) functions or components, innovations in technology, additional capabilities.
CONNECTIVITY | The ability or ease with which communication connections, charging connections, and physical interfaces can be connected to peripheral devices.


## Annotation Schema

Each comparison is annotated as a quadruple in the following JSON-like format:

{

    "subject": "Apple iPhone 15",
    
    "object": "Apple iPhone 13",
    
    "category": "OS#PERFORMANCE",
    
    "preference": "better"
    
}


A single comment may contain multiple such comparison quadruples.

### Subject

The **subject** refers to the phone being reviewed. It is typically provided as structured metadata (e.g., product title on the e-commerce platform).

* Format: Brand + Model (e.g., “Apple iPhone 15”, “Huawei P60”)

* Annotation Guideline:
    * The subject phone is not inferred from the comment itself, but is known from metadata.
    * It is fixed per comment and remains constant across all extracted quadruples from the same comment.

* Examples
    * This is a review for Apple iPhone 13: The appearance is similar to iPhone 12, and it runs much smoother! → {Apple iPhone 13}
        * Explanation: The phone being reviewed can be retrieved directly from e-commerce metadata and is provided alongside the comment.

### Object

The **object** refers to another phone that the subject is compared to.

* Format: Brand + Model, even if abbreviated or partially mentioned in the comment.

* Annotation Guideline:
    * The object must correspond to a valid smartphone model.
    * Generic categories like "Android phon" or "iOS device" are not allowed.
    * When the brand is not mentioned, infer it if possible based on model conventions.

* Examples
    * This is a review for Huawei nova9 SE: It's already nova9, but it has fewer features than nova7.  → {Huawei nova7}
        * Explanation: The comment compares the subject to “nova7”, and based on context and known product series, it is inferred to be “Huawei nova7”.
    * This is a review for vivo X100 Pro: Display and audio—screen feels about the same as mate60, sound is decent. Camera—amazing shots, beautiful portraits, comes with beautify mode. → {Huawei Mate 60}
        * Explanation: The subject is compared to “mate60”, and based on model naming conventions, “Mate” refers to a Huawei product line, hence the object is annotated as “Huawei Mate 60”.

### Category

The **category** describes the aspect under comparison, following the Entity#Attribute format.

* Format: ENTITY#ATTRIBUTE(e.g., OS#PERFORMANCE, DISPLAY#QUALITY, CAMERA#GENERAL)

* Annotation Guideline:
    * Adopt a two-level hierarchical taxonomy.
    * Use the most specific entity + attribute available.
    * When unclear, assign #GENERAL to denote overall evaluation of the entity.

* Examples
    * This is a review for Meizu 21: Apart from not having a 2k screen, everything else is amazing. The audio quality is a huge step up from 20Pro. → {AUDIO DEVICES#QUALITY}
        * Explanation: The comparison is about “audio”, which maps to the entity “AUDIO DEVICES”. The attribute mentioned is clearly about perceived quality.
    * This is a review for Apple iPhone 15 Pro: Got it during the Double Eleven sale—great price. Compared to iPhone 14, the camera has improved. → {CAMERA#GENERAL}
        * The comment discusses improvements in “camera” without detailing whether it's about quality or performance, so it is labeled under “GENERAL”.
      
### Preference

The **preference** indicates the comparative outcome between subject and object.

* Must be one of the following three labels:
    * better – subject is preferred over object
    * worse – subject is inferior to object
    * equal – subject and object are considered similar

* Annotation Guideline:
    * Expressed preference must be clearly implied or explicitly stated.

* Examples
    * This is a review for Huawei nova9 SE: It's already nova9, but it has fewer features than nova7. → {worse}
        * Explanation: The reviewer believes the subject is inferior to the object in terms of features, so the preference is annotated as “worse”.
    * This is a review for Meizu 21: Apart from not having a 2k screen, everything else is amazing. The audio quality is a huge step up from 20Pro. → {better}
        * Explanation: The comment suggests the subject has significantly better audio than the object, so the preference is “better”.
    * This is a review for vivo X100 Pro: Display and audio—screen feels about the same as mate60, sound is decent. Camera—amazing shots, beautiful portraits, comes with beautify mode. → {equal}
        Explanation: The reviewer states that the display is “about the same” as mate60, suggesting equality in performance, hence the preference is “equal”.


## Automated annotation process
<!-- 
用于 SOCP 任务的自动化标注流程分为两个主要阶段：Subject-Object-Aspect-Preference四元组的提取和方面类别的分类。通过这种两步法，prompt会简化，并使 LLM能够更高效地完成每个子任务，从而提升提取过程的准确性。
通过这种两步法，prompt会简化，并使 LLM能够更高效地完成每个子任务，从而提升提取过程的准确性。

我们首先选取比较评论，指导 LLM 逐步提取比较主体、比较客体、比较方面以及比较偏好。
随后，我们将这一指导过程作为历史信息提供给 LLM，使它具备识别比较要素的能力。在拥有历史标注作为上下文的情况下，我们只需输入新的评论文本，LLM 便能直接提取其中的比较要素。下表展示了这一指导流程。

在提取完比较四元组之后，下一阶段是将其中的方面元素分类到预先定义的类别。下面展示了方面类别分类的提示。
-->


The automated annotation process for the SOCP task is divided into two main phases: **Subject-Object-Aspect-Preference Quadruplet Extraction** and **Aspect Category Classification**. 
This two-step approach simplifies the prompt, enabling the LLM to handle each task more efficiently and improving the accuracy of the extraction process.
<br>
<br>

### Subject-Object-Aspect-Preference Quadruplet Extraction

We first select comparison reviews and guide the LLM to extract the comparative subject, comparative object, comparative aspect, and comparative preference step by step. 
This guiding process is then provided as historical information to the LLM, enabling it to extract the comparative elements. 
With historical annotations as context, we can directly input new review texts, allowing the LLM to extract the comparative elements. The following table shows the guiding process.
<br>

Role | Conversation
---- | ----
Human | Here’s a review of the Google Pixel 6 Pro: “...It surpasses the Samsung Galaxy S21 Ultra especially in terms of photographic detail. it also has a great processor performance and runs smoother compared to the iPhone 13...” Which other phone models were compared with the Google Pixel 6 Pro in the review?
LLM | The Google Pixel 6 Pro was compared with the following smartphones: Samsung Galaxy S21 Ultra and Apple iPhone 13.
Human | In the reviews, which smartphone features were compared between the Google Pixel 6 Pro and others? Did the Google Pixel 6 Pro perform better, worse, or the Equal?
LLM | In the reviews, the Google Pixel 6 Pro was compared with other smartphones in the following aspects: Camera Performance: Compared to the Samsung Galaxy S21 Ultra, the Google Pixel 6 Pro’s camera is better at capturing details. Processor Performance: Compared to the iPhone 13, the Google Pixel 6 Pro’s processor performance is superior and runs more smoothly.
Human | Great, now you need to organize the results into JSON format as follows: \{”subject”: The smartphone purchased, ”object”: The other smartphone models being compared, ”aspect”: The smartphone attribute being compared, ”preference”: Indicates whether the purchased smartphone is better, worse, or the Equal\}. Each JSON object represents one comparison. Note that ”preference” can only be one of ”BETTER,” ”WORSE,” or ”Equal.”
LLM | \[\{”subject”: ”Google Pixel 6 Pro”, ”object”: ”Samsung Galaxy S21 Ultra”, ”aspect”: ”Camera Performance”, ”preference”: ”BETTER”}, {”subject”: ”Google Pixel 6 Pro”, ”object”: ”Apple iPhone 13”, ”aspect”: ”Processor Performance”, ”preference”: ”BETTER”\}\]
Human | Great! Next, I will provide you with some reviews, each review being independent. You need to output the results in JSON format according to the above requirements. If the review does not directly mention other phone models for comparison, output [].
LLM | Of course, I am ready. Please provide the phone reviews, and I will convert them into JSON format according to your requirements.
Human | Here’s a review of the Samsung Z Flip5: “The packaging was intact, the shipping was fast, the seller’s service was good, it’s compact and exquisite, highly functional, and the price is also more favorable than in physical stores.”
LLM | []
Human | {A review text}

<br>

## Aspect Category Classification

After extracting the comparison quaternions, the next phase involves categorizing the aspect element into predefined categories. 
The prompt of Aspect Category Classification is shown below:
<br>
<br>
In ABSA tasks within the mobile phone domain, the aspect category is defined by concatenating Entity and Attribute in the format Entity#Attribute. <br>
Entity must be selected from the list: {the list of predefined entity labels}, and Attribute must be chosen from the list: {the list of predefined attribute labels}.<br>
Given a review and a list of comparative aspects, please determine the category for each aspect in the list. Output a list (e.g., \[Entity\#Attribute\]) without any explanation. <br>
Review: “\{review text\}”. <br>
Aspect: \{the list of aspects\}.<br>
Output:

