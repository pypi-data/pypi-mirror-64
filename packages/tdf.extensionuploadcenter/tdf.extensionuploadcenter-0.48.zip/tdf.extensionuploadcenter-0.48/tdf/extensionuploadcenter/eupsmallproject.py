# -*- coding: utf-8 -*-
from tdf.extensionuploadcenter import _
import re
from collective import dexteritytextindexer
from plone.supermodel import model
from zope import schema
from plone.app.textfield import RichText
from plone.autoform import directives
from plone.supermodel.directives import primary
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope.interface import Invalid, invariant
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.interface import directlyProvides
from zope.schema.interfaces import IContextSourceBinder
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory
from plone.indexer.decorator import indexer
from zope.security import checkPermission
from plone import api
from z3c.form import validator
from plone.dexterity.browser.view import DefaultView
from tdf.extensionuploadcenter import quote_chars
from plone.uuid.interfaces import IUUID
from Products.validation import V_REQUIRED


checkfileextension = re.compile(
    r"^.*\.(oxt|OXT)").match


checkEmail = re.compile(
    r"[a-zA-Z0-9._%-]+@([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,4}").match


def validateEmail(value):
    if not checkEmail(value):
        raise Invalid(_(u"Invalid email address"))
    return True


def vocabCategories(context):
    # For add forms

    # For other forms edited or displayed
    from tdf.extensionuploadcenter.eupcenter import IEUpCenter
    while context is not None and not IEUpCenter.providedBy(context):
        # context = aq_parent(aq_inner(context))
        context = context.__parent__

    category_list = []
    if context is not None and context.available_category:
        category_list = context.available_category

    terms = []
    for value in category_list:
        terms.append(SimpleTerm(value, token=value.encode('unicode_escape'),
                                title=value))

    return SimpleVocabulary(terms)


directlyProvides(vocabCategories, IContextSourceBinder)


def vocabAvailLicenses(context):
    """ pick up licenses list from parent """
    from tdf.extensionuploadcenter.eupcenter import IEUpCenter
    while context is not None and not IEUpCenter.providedBy(context):
        # context = aq_parent(aq_inner(context))
        context = context.__parent__

    license_list = []
    if context is not None and context.available_licenses:
        license_list = context.available_licenses
    terms = []
    for value in license_list:
        terms.append(SimpleTerm(value, token=value.encode('unicode_escape'),
                                title=value))
    return SimpleVocabulary(terms)


directlyProvides(vocabAvailLicenses, IContextSourceBinder)


def vocabAvailVersions(context):
    """ pick up the program versions list from parent """
    from tdf.extensionuploadcenter.eupcenter import IEUpCenter
    while context is not None and not IEUpCenter.providedBy(context):
        # context = aq_parent(aq_inner(context))
        context = context.__parent__

    versions_list = []
    if context is not None and context.available_versions:
        versions_list = context.available_versions

    terms = []
    for value in versions_list:
        terms.append(SimpleTerm(value, token=value.encode('unicode_escape'),
                                title=value))
    return SimpleVocabulary(terms)


directlyProvides(vocabAvailVersions, IContextSourceBinder)


def isNotEmptyCategory(value):
    if not value:
        raise Invalid(u'You have to choose at least one category for your '
                      u'project.')
    return True


def vocabAvailPlatforms(context):
    """ pick up the list of platforms from parent """
    from tdf.extensionuploadcenter.eupcenter import IEUpCenter
    while context is not None and not IEUpCenter.providedBy(context):
        # context = aq_parent(aq_inner(context))
        context = context.__parent__

    platforms_list = []
    if context is not None and context.available_platforms:
        platforms_list = context.available_platforms
    terms = []
    for value in platforms_list:
        terms.append(SimpleTerm(value, token=value.encode('unicode_escape'),
                                title=value))
    return SimpleVocabulary(terms)


directlyProvides(vocabAvailPlatforms, IContextSourceBinder)


def validateextensionfileextension(value):
    if not checkfileextension(value.filename):
        raise Invalid(u'You could only upload LibreOffice extension files '
                      u'with a proper file extension.\n'
                      u'LibreOffice extensions have an \'oxt\' file '
                      u'extension.')
    return True


yesnochoice = SimpleVocabulary(
    [SimpleTerm(value=0, title=_(u'No')),
     SimpleTerm(value=1, title=_(u'Yes')), ]
)


@provider(IContextAwareDefaultFactory)
def legal_declaration_title(context):
    return context.title_legaldisclaimer


@provider(IContextAwareDefaultFactory)
def legal_declaration_text(context):
    return context.legal_disclaimer


@provider(IContextAwareDefaultFactory)
def allowedeupimagefileextensions(context):
    return context.allowed_eupimagefileextension.replace("|", ", ")


def validateimagefileextension(value):
    catalog = api.portal.get_tool(name='portal_catalog')
    result = catalog.uniqueValuesFor('allowedeupimagefileextensions')
    pattern = r'^.*\.({0})'.format(result[0])
    matches = re.compile(pattern, re.IGNORECASE).match
    if not matches(value.filename):
        raise Invalid(
            u'You could only upload files with an allowed file extension. '
            u'Please try again to upload a file with the correct file'
            u'extension.')
    return True


@provider(IContextAwareDefaultFactory)
def allowedeupdocfileextensions(context):
    return context.allowed_docfileextension.replace("|", ", ")


def validatedocfileextension(value):
    catalog = api.portal.get_tool(name='portal_catalog')
    result = catalog.uniqueValuesFor('allowedeupdocfileextensions')
    pattern = r'^.*\.({0})'.format(result[0])
    matches = re.compile(pattern, re.IGNORECASE).match
    if not matches(value.filename):
        raise Invalid(
            u'You could only upload documentation files with an allowed '
            u'file extension. Please try again to upload a file with the '
            u'correct file extension.')
    return True


class AcceptLegalDeclaration(Invalid):
    __doc__ = _(u"It is necessary that you accept the Legal Declaration")


class IEUpSmallProject(model.Schema):
    directives.mode(information="display")
    information = schema.Text(
        title=_(u"Information"),
        description=_(u"The Dialog to create a new project consists of "
                      u"different register. Please go through this register "
                      u"and fill in the appropriate data for your project or "
                      u"choose one of the options that are provided. You "
                      u"could upload one or more files to your project on "
                      u"the register 'File Upload' and 'Optional Further "
                      u"File Upload'.")
    )

    dexteritytextindexer.searchable('title')
    title = schema.TextLine(
        title=_(u"Title"),
        description=_(u"Project Title - minimum 5 and maximum 50 characters"),
        min_length=5,
        max_length=50
    )

    dexteritytextindexer.searchable('description')
    description = schema.Text(
        title=_(u"Project Summary"),
    )

    dexteritytextindexer.searchable('details')
    primary('details')
    details = RichText(
        title=_(u"Full Project Description"),
        required=False
    )
    model.fieldset('category_compatibility',
                   label=u"Categories / Compatibility",
                   fields=['category_choice', 'compatibility_choice']
                   )

    model.fieldset('legal',
                   label=u"Legal",
                   fields=['licenses_choice',
                           'title_declaration_legal',
                           'declaration_legal',
                           'accept_legal_declaration',
                           'source_code_inside',
                           'link_to_source']
                   )

    directives.widget(licenses_choice=CheckBoxFieldWidget)
    licenses_choice = schema.List(
        title=_(u'License of the uploaded file'),
        description=_(u"Please mark one or more licenses you publish your "
                      u"release."),
        value_type=schema.Choice(source=vocabAvailLicenses),
        required=True,
    )

    directives.mode(title_declaration_legal='display')
    title_declaration_legal = schema.TextLine(
        title=_(u""),
        required=False,
        defaultFactory=legal_declaration_title
    )

    directives.mode(declaration_legal='display')
    declaration_legal = schema.Text(
        title=_(u""),
        required=False,
        defaultFactory=legal_declaration_text
    )

    accept_legal_declaration = schema.Bool(
        title=_(u"Accept the above legal disclaimer"),
        description=_(u"Please declare that you accept the above legal "
                      u"disclaimer."),
        required=True
    )

    source_code_inside = schema.Choice(
        title=_(u"Is the source code inside the extension?"),
        vocabulary=yesnochoice,
        required=True
    )

    link_to_source = schema.URI(
        title=_(u"Please fill in the Link (URL) to the Source Code."),
        required=False
    )

    dexteritytextindexer.searchable('category_choice')
    directives.widget(category_choice=CheckBoxFieldWidget)
    category_choice = schema.List(
        title=_(u"Choose your categories"),
        description=_(u"Please select the appropriate categories (one or "
                      u"more) for your project."),
        value_type=schema.Choice(source=vocabCategories),
        constraint=isNotEmptyCategory,
        required=True
    )

    contactAddress = schema.TextLine(
        title=_(u"Contact email-address"),
        description=_(u"Contact email-address for the project."),
        constraint=validateEmail
    )

    directives.mode(eupimageextension='display')
    eupimageextension = schema.TextLine(
        title=_(u'The following file extensions are allowed for screenshot '
                u'files (upper case and lower case and mix of both):'),
        defaultFactory=allowedeupimagefileextensions,
    )

    screenshot = NamedBlobImage(
        title=_(u"Screenshot of the Extension"),
        description=_(u"Add a screenshot by clicking the 'Browse' button. "
                      u"You could provide an image of the file format 'png', "
                      u"'gif' or 'jpg'."),
        required=True,
        constraint=validateimagefileextension
    )

    releasenumber = schema.TextLine(
        title=_(u"Versions Number"),
        description=_(u"Version Number of the Extension File (up to twelf "
                      u"chars) which you upload in this project."),
        default=_(u"1.0"),
        max_length=12,
    )

    directives.widget(compatibility_choice=CheckBoxFieldWidget)
    compatibility_choice = schema.List(
        title=_(u"Compatible with versions of LibreOffice"),
        description=_(u"Please mark one or more program versions with which "
                      u"this release is compatible with."),
        value_type=schema.Choice(source=vocabAvailVersions),
        required=True,
        default=[]
    )

    file = NamedBlobFile(
        title=_(u"The first file you want to upload."),
        description=_(u"Please upload your file."),
        required=True,
        constraint=validateextensionfileextension,
    )

    directives.widget(platform_choice=CheckBoxFieldWidget)
    platform_choice = schema.List(
        title=_(u"First uploaded file is compatible with the Platform(s)"),
        description=_(u"Please mark one or more platforms with which the "
                      u"uploaded file is compatible."),
        value_type=schema.Choice(source=vocabAvailPlatforms),
        required=True,
    )
    model.fieldset('documentation',
                   label='Documentation',
                   fields=['documentation_link', 'eupdocextension',
                           'documentation_file']
                   )

    documentation_link = schema.URI(
        title=_(u"URL of documentation repository "),
        description=_(u"If the project has externally hosted "
                      u"documentation, enter its URL "
                      u"(example: 'http://www.mysite.org')."),
        required=False
    )

    directives.mode(eupdocextension='display')
    eupdocextension = schema.TextLine(
        title=_(u'The following file extensions are allowed for documentation '
                u'files (upper case and lower case and mix of both):'),
        defaultFactory=allowedeupdocfileextensions,
    )

    documentation_file = NamedBlobFile(
        title=_(u"Dokumentation File"),
        description=_(u"If you have a Documentation in the file format 'PDF' "
                      u"or 'ODT' you could add it here."),
        required=False,
        constraint=validatedocfileextension
    )

    model.fieldset('fileset1',
                   label=u"File Upload",
                   fields=['filetitlefield', 'platform_choice', 'file', ]
                   )

    directives.mode(filetitlefield='display')
    filetitlefield = schema.TextLine(
        title=_(u"The First File You Want To Upload"),
        description=_(u"You need only to upload one file to your project. "
                      u"There are options for further two file uploads "
                      u"if you want to provide files for different "
                      u"platforms.")
    )

    model.fieldset('fileset2',
                   label=u"Optional Further File Upload",
                   fields=['filetitlefield1', 'platform_choice1', 'file1',
                           'filetitlefield2', 'platform_choice2', 'file2']
                   )

    directives.mode(filetitlefield1='display')
    filetitlefield1 = schema.TextLine(
        title=_(u"Second Release File"),
        description=_(u"Here you could add an optional second file to your "
                      u"project, if the files support different "
                      u"platforms.")
    )

    directives.widget(platform_choice1=CheckBoxFieldWidget)
    platform_choice1 = schema.List(
        title=_(u"Second uploaded file is compatible with the Platform(s)"),
        description=_(u"Please mark one or more platforms with which the "
                      u"uploaded file is compatible."),
        value_type=schema.Choice(source=vocabAvailPlatforms),
        required=False,
    )

    file1 = NamedBlobFile(
        title=_(u"The second file you want to upload (this is optional)"),
        description=_(u"Please upload your file."),
        required=False,
        constraint=validateextensionfileextension,
    )

    directives.mode(filetitlefield2='display')
    filetitlefield2 = schema.TextLine(
        title=_(u"Third Release File"),
        description=_(u"Here you could add an optional third file to your "
                      u"project, if the files support different platforms.")
    )

    directives.widget(platform_choice2=CheckBoxFieldWidget)
    platform_choice2 = schema.List(
        title=_(u"Third uploaded file is compatible with the Platform(s))"),
        description=_(u"Please mark one or more platforms with which the "
                      u"uploaded file is compatible."),
        value_type=schema.Choice(source=vocabAvailPlatforms),
        required=False,
    )

    file2 = NamedBlobFile(
        title=_(u"The third file you want to upload (this is optional)"),
        description=_(u"Please upload your file."),
        required=False,
        constraint=validateextensionfileextension,
    )

    @invariant
    def licensenotchoosen(value):
        if not value.licenses_choice:
            raise Invalid(_(u"Please choose a license for your release."))

    @invariant
    def compatibilitynotchoosen(data):
        if not data.compatibility_choice:
            raise Invalid(_(u"Please choose one or more compatible product "
                            u"versions for your release."))

    @invariant
    def legaldeclarationaccepted(data):
        if data.accept_legal_declaration is not True:
            raise AcceptLegalDeclaration(
                _(u"Please accept the Legal Declaration about your Release "
                  u"and your Uploaded File"))

    @invariant
    def testingvalue(data):
        if data.source_code_inside is not 1 and data.link_to_source is None:
            raise Invalid(_(u"You answered the question, whether the source "
                            u"code is inside your extension with no "
                            u"(default answer). If this is the correct "
                            u"answer, please fill in the Link (URL) to the "
                            u"Source Code."))

    @invariant
    def noOSChosen(data):
        if data.file is not None and data.platform_choice == []:
            raise Invalid(_(u"Please choose a compatible platform for the "
                            u"uploaded file."))


@indexer(IEUpSmallProject)
def release_number(context, **kw):
    return context.releasenumber


@indexer(IEUpSmallProject)
def project_compat_versions(context, **kw):
    return context.compatibility_choice


def notifyProjectManager(self, event):
    state = api.content.get_state(self)
    if self.__parent__.contactForCenter is not None:
        mailrecipient = str(self.__parent__.contactForCenter)
    else:
        mailrecipient = 'extensions@libreoffice.org'
    api.portal.send_email(
        recipient="{}".format(self.contactAddress),
        sender=u"{} <{}>".format('Admin of the Website', mailrecipient),
        subject=u"Your Project {}".format(self.title),
        body=(u"The status of your LibreOffice extension project changed. "
              u"The new status is {}").format(state)
    )


def notifyAboutNewReviewlistentry(self, event):
    state = api.content.get_state(self)
    if self.__parent__.contactForCenter is not None:
        mailrecipient = str(self.__parent__.contactForCenter)
    else:
        mailrecipient = 'extensions@libreoffice.org'

    if state == "pending":
        api.portal.send_email(
            recipient=mailrecipient,
            subject=(u"A Project with the title {} was added to the review "
                     u"list").format(self.title),
            body="Please have a look at the review list and check if the "
                 "project is ready for publication. \n"
                 "\n"
                 "Kind regards,\n"
                 "The Admin of the Website"
        )


def textmodified_project(self, event):
    state = api.content.get_state(self)
    if self.__parent__.contactForCenter is not None:
        mailrecipient = str(self.__parent__.contactForCenter)
    else:
        mailrecipient = 'extensions@libreoffice.org'
    if state == "published":
        if self.details is not None:
            detailed_description = self.details.output
        else:
            detailed_description = None

        api.portal.send_email(
            recipient=mailrecipient,
            sender=u"{} <{}>".format('Admin of the Website', mailrecipient),
            subject=(u"The content of the project {} has "
                     u"changed").format(self.title),
            body=(u"The content of the project {} has changed. Here you get "
                  u"the text of the description field of the project: "
                  u"\n'{}\n\nand this is the text of the details field:"
                  u"\n{}'").format(self.title,
                                   self.description,
                                   detailed_description),
        )


def notifyAboutNewProject(self, event):
    if self.__parent__.contactForCenter is not None:
        mailrecipient = str(self.__parent__.contactForCenter),
    else:
        mailrecipient = 'extensions@libreoffice.org'
    api.portal.send_email(
        recipient=mailrecipient,
        subject=u"A Project with the title {} was added".format(self.title),
        body="A member added a new project"
    )


class ValidateEUpSmallProjectUniqueness(validator.SimpleFieldValidator):
    # Validate site-wide uniqueness of project titles.

    def validate(self, value):
        # Perform the standard validation first
        from tdf.extensionuploadcenter.eupproject import IEUpProject

        super(ValidateEUpSmallProjectUniqueness, self).validate(value)
        if value is not None:
            catalog = api.portal.get_tool(name='portal_catalog')
            results1 = catalog({'Title': quote_chars(value),
                                'object_provides':
                                    IEUpProject.__identifier__, })
            results2 = catalog({'Title': quote_chars(value),
                                'object_provides':
                                    IEUpSmallProject.__identifier__, })
            results = results1 + results2

            contextUUID = IUUID(self.context, None)
            for result in results:
                if result.UID != contextUUID:
                    raise Invalid(_(u"The project title is already in use."))


validator.WidgetValidatorDiscriminators(
    ValidateEUpSmallProjectUniqueness,
    field=IEUpSmallProject['title'],
)


class EUpSmallProjectView(DefaultView):
    def canPublishContent(self):
        return checkPermission('cmf.ModifyPortalContent', self.context)

    def releaseLicense(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        path = "/".join(self.context.getPhysicalPath())
        idx_data = catalog.getIndexDataForUID(path)
        licenses = idx_data.get('releaseLicense')
        return (r for r in licenses)

    def releaseCompatibility(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        path = "/".join(self.context.getPhysicalPath())
        idx_data = catalog.getIndexDataForUID(path)
        compatibility = idx_data.get('getCompatibility')
        return (r for r in compatibility)

    def projectCategory(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        path = "/".join(self.context.getPhysicalPath())
        idx_data = catalog.getIndexDataForUID(path)
        category = idx_data.get('getCategories')
        return (r for r in category)

    def latest_release_date(self):
        return None
